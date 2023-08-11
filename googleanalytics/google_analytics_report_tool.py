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
    start_date_of_query: str = Field(..., description="The starting date of the query, in YYYY-MM-DD format")
    end_date_of_query: str = Field(..., description="The last date of the query, in YYYY-MM-DD format, if today, return today's date")
    store_report_in_single_file: bool= Field(..., description="True if it is specified that the report should be stored in a single file. False otherwise.")


class GoogleAnalyticsReportTool(BaseTool):
    """
    Analytics Report Tool
    """
    name: str = "Google Analytics Report Tool"
    args_schema: Type[BaseModel] = GoogleAnalyticsReportToolInput
    description: str = "Return a google analytics report for the information the user requires"
    resource_manager: Optional[FileManager] = None

    def _execute(self, start_date_of_query: str, end_date_of_query: str, store_report_in_single_file: bool):
        property_id = int(self.get_tool_config("PROPERTY_ID"))
        google_credentials = self.get_tool_config("GOOGLE_CREDENTIALS_FILE")

        self._set_google_credentials(google_credentials)

        client = BetaAnalyticsDataClient()
        dimensions_and_metrics = self.get_dimensions_and_metrics()

        filenames = ["report.txt"] if store_report_in_single_file else []
        report=""

        for dimensions, metrics in dimensions_and_metrics:
            request = self._create_run_report_request(property_id, dimensions, metrics, start_date_of_query, end_date_of_query)
            google_response = client.run_report(request)
            report = report + self._generate_report(google_response)

            if not store_report_in_single_file:
                filename = self._generate_filename(dimensions, metrics, filenames)
                filenames.append(filename)
                self.resource_manager.write_file(filename, report)
                report = ""

        if store_report_in_single_file:
            self.resource_manager.write_file(filenames[0], report)

        os.remove("credentials.json")

        response = "Successfully wrote " + ", ".join(filenames) + "."
        return response

    def _generate_report(self, google_response):
        report = ""
        for dimension_header in google_response.dimension_headers:
            report += dimension_header.name + " "
        for metric_header in google_response.metric_headers:
            report += metric_header.name + " "
        report += '\n'

        for row in google_response.rows:
            for dimension_value in row.dimension_values:
                report += dimension_value.value + " "
            for metric_value in row.metric_values:
                report += metric_value.value + " "
            report += '\n'
        return report

    def _set_google_credentials(self, credentials: str):
        writable_credentials = json.loads(json.loads(credentials))
        with open("credentials.json", "w") as outfile:
            json.dump(writable_credentials, outfile)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"

    def _generate_filename(self, dimensions, metrics, filenames):
        filename = dimensions[0] + metrics[0]
        if filename in filenames:
            filename = filename + "New"
        filename = filename + ".txt"
        return filename

    def _create_run_report_request(self, property_id, dimensions, metrics, start_date_of_query, end_date_of_query):
        metrics_list = [Metric(name=metric) for metric in metrics]
        dimensions_list = [Dimension(name=dimension) for dimension in dimensions]
        return RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=dimensions_list,
            metrics=metrics_list,
            date_ranges=[DateRange(start_date=start_date_of_query, end_date=end_date_of_query)],
            limit=100000,
            offset=0,
        )

    def get_dimensions_and_metrics(self):
        dimensions_and_metrics = []
        with open("config.yaml", "r") as file:
            dict = yaml.load(file, Loader=yaml.SafeLoader)
            for lists in dict["GOOGLE_ANALYTICS_VARIABLES"]:
                dimensions_and_metrics.append([lists["Dimension"], lists["Metric"]])
            return dimensions_and_metrics