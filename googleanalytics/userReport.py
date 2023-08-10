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

class GoogleAnalyticsReportToolInput(BaseModel):
    start: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end: str = Field(..., description="The last date of the query, in YYYY-MM-DD format, if today, return today's date")
    is_single_file: bool= Field(..., description="True if it is specified that the report should be stored in a single file. False otherwise.")


class GoogleAnalyticsReportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Analytics Report Tool"
    args_schema: Type[BaseModel] = GoogleAnalyticsReportToolInput
    description: str = "Return a google analytics report for the information the user requires"
    resource_manager: Optional[FileManager] = None

    def _execute(self, start: str, end: str, is_single_file: bool):
        property_id = int(self.get_tool_config("PROPERTY_ID"))
        google_credentials = self.get_tool_config("GOOGLE_CREDENTIALS_FILE")

        self._set_google_credentials(google_credentials)

        client = BetaAnalyticsDataClient()
        dim_metrics = self.return_dim_metrics()
        list_of_names = ["report.txt"] if is_single_file else []

        for dimensions, metrics in dim_metrics:
            if not is_single_file:
                filename = self._generate_filename(dimensions, metrics, list_of_names)
                list_of_names.append(filename)

            request = self._create_run_report_request(property_id, dimensions, metrics, start, end)
            response = client.run_report(request)
            report = self._generate_report(response)

            if not is_single_file:
                self._write_to_file(filename, report)
                report = ""

        if is_single_file:
            self._write_to_file(list_of_names[0], report)

        os.remove("sample.json")

        response_str = " ".join(list_of_names) + "."
        return "Successfully wrote " + response_str

    def _generate_report(self, response):
        report = ""
        for dimension_header in response.dimension_headers:
            report += dimension_header.name + " "
        for metric_header in response.metric_headers:
            report += metric_header.name + " "
        report += '\n'

        for row in response.rows:
            for dimension_value in row.dimension_values:
                report += dimension_value.value + " "
            for metric_value in row.metric_values:
                report += metric_value.value + " "
            report += '\n'
        return report

    def _set_google_credentials(self, credentials: str):
        writable_credentials = json.loads(json.loads(credentials))
        with open("sample.json", "w") as outfile:
            json.dump(writable_credentials, outfile)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sample.json"

    def _generate_filename(self, dimensions, metrics, list_of_names):
        filename = dimensions[0] + metrics[0]
        if filename in list_of_names:
            filename = filename + "New"
        filename = filename + ".txt"
        return filename

    def _create_run_report_request(self, property_id, dimensions, metrics, start, end):
        metrics_list = [Metric(name=x) for x in metrics]
        dimensions_list = [Dimension(name=x) for x in dimensions]
        return RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=dimensions_list,
            metrics=metrics_list,
            date_ranges=[DateRange(start_date=start, end_date=end)],
            limit=100000,
            offset=0,
        )

    def return_dim_metrics(self):
        dim_metrics = []
        # try:
        with open("config.yaml", "r") as file:
            dict = yaml.load(file, Loader=yaml.SafeLoader)
            for lists in dict["GOOGLE_ANALYTICS_VARIABLES"]:
                dim_metrics.append([lists["Dimension"], lists["Metric"]])
            return dim_metrics