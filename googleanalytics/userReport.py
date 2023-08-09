import os
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
import json
from typing import Type, Optional
from superagi.resource_manager.file_manager import FileManager
import yaml
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

class UserReportInput(BaseModel):
    start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end: str = Field(..., description="The last date of the query, in YYYY-MM-DD format, if today, return today's date")
    issinglefile: bool= Field(..., description="True if it is specified that the report should be stored in a single file. False otherwise.")


class reportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Analytics Report Tool"
    args_schema: Type[BaseModel] = UserReportInput
    description: str = "Return a google analytics report for the information the user requires"
    resource_manager: Optional[FileManager] = None

    def _execute(self, start: str, end: str, issinglefile: bool):

        property=int(self.get_tool_config("PROPERTY_ID"))
        dict = self.get_tool_config("GOOGLE_CREDENTIALS_FILE")

        writable = json.loads(json.loads(dict))
        with open("sample.json", "w") as outfile:
            json.dump(writable, outfile)
        os.environ[
            'GOOGLE_APPLICATION_CREDENTIALS'] = "sample.json"

        client = BetaAnalyticsDataClient()

        DimMetrics = self.returnDimMetrics()
        listofnames=[]
        if issinglefile:
            listofnames.append("report.txt")

        report=""

        for dimensions,metrics in DimMetrics:
            if not issinglefile:
                filename = dimensions[0]+metrics[0]
                if filename in listofnames:
                    filename=filename+"New"
                filename=filename+".txt"
                listofnames.append(filename)

            mi=[]
            for x in metrics:
                mi.append(Metric(name=x))

            di=[]
            for x in dimensions:
                di.append(Dimension(name=x))

            request = RunReportRequest(
                property=f"properties/{property}",
                dimensions=di,
                metrics=mi,
                date_ranges=[DateRange(start_date=start, end_date=end)],
                limit=100000,
                offset=0,
            )
            response = client.run_report(request)

            for dimensionHeader in response.dimension_headers:
                report= report+ dimensionHeader.name + " "
            for metricHeader in response.metric_headers:
                report= report + metricHeader.name +" "

            report= report+'\n'

            for row in response.rows:
                for dimension_value in row.dimension_values:
                    report = report +dimension_value.value +" "

                for metric_value in row.metric_values:
                    report= report+ metric_value.value+ " "
                report = report + '\n'

            if not issinglefile:
                self.resource_manager.write_file(filename, report)
                report=""

        if issinglefile:
            self.resource_manager.write_file(listofnames[0], report)

        os.remove("sample.json")

        response = ""
        for name in listofnames:
            response=response +" "+ name+","

        response=response[:-1]+"."

        return "Succesfully wrote"+response

    def returnDimMetrics(self):
        DimMetrics = []
        # try:
        # with open("superagi/tools/marketplace_tools/googleanalytics/config.yaml", "r") as file:
        with open("superagi/tools/external_tools/google-analytics-tool-superagi/config.yaml", "r") as file:
            dict = yaml.load(file, Loader=yaml.SafeLoader)
            for lists in dict["list"]:
                DimMetrics.append([lists["Dimension"], lists["Metric"]])
            return DimMetrics
        # except:
        #     return [[['pageTitle'], ['totalUsers']], [
        #         ['deviceModel', 'deviceCategory'], ['totalUsers']], [['dateHour'],
        #                                                              ['totalUsers', 'averageSessionDuration',
        #                                                               'bounceRate']], [['sourceMedium'],
        #                                                                                ['totalUsers']]]