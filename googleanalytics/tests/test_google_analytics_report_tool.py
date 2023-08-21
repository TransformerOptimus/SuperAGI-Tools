import unittest
from unittest.mock import patch, Mock, call
from pydantic import ValidationError
import json
from superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool import GoogleAnalyticsReportTool, GoogleAnalyticsReportToolInput
from google.analytics.data_v1beta.types import RunReportRequest

class TestGoogleAnalyticsReportTool(unittest.TestCase):


    @patch("superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool.json")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool.os")
    @patch("superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool.BetaAnalyticsDataClient") 
    def test_set_google_credentials(self, mock_beta_cli, mock_os, mock_open, mock_json):
        tool = GoogleAnalyticsReportTool()
        
        mock_json.loads.side_effect = ['credentials', {"PROPERTY_ID":"value1", "GOOGLE_CREDENTIALS_FILE":"value2"}]
        tool._set_google_credentials('credentials')
            
        calls = [call('credentials'), call('credentials')]
        mock_json.loads.assert_has_calls(calls)
        mock_open.assert_called_once_with("credentials.json", "w")
        mock_json.dump.assert_called_once_with({"PROPERTY_ID":"value1", "GOOGLE_CREDENTIALS_FILE":"value2"}, mock_open.return_value.__enter__.return_value)
        mock_os.environ.__setitem__.assert_called_once_with('GOOGLE_APPLICATION_CREDENTIALS', "credentials.json")

    def test_args_schema(self):
        with self.assertRaises(ValidationError):
            GoogleAnalyticsReportToolInput()

    @patch("superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool.BetaAnalyticsDataClient")
    def test_create_run_report_request(self, mock_client):
        tool = GoogleAnalyticsReportTool()
        request = tool._create_run_report_request(
            12345,
            ['dimension1', 'dimension2'],
            ['metric1', 'metric2'],
            '2021-07-01',
            '2021-07-31'
        )
        self.assertIsInstance(request, RunReportRequest)
        self.assertEqual(request.property, "properties/12345")
        self.assertEqual(len(request.dimensions), 2)
        self.assertEqual(len(request.metrics), 2)

    def test_generate_report(self):
        tool = GoogleAnalyticsReportTool()
        mock_response = Mock(
            dimension_headers=[Mock(name="dimension1"), Mock(name="dimension2")],
            metric_headers=[Mock(name="metric1"), Mock(name="metric2")],
            rows=[
                Mock(
                    dimension_values=[Mock(value="dvalue1"), Mock(value="dvalue2")],
                    metric_values=[Mock(value="mvalue1"), Mock(value="mvalue2")]
                )
            ]
        )
        mock_response.dimension_headers[0].name = "dimension1"
        mock_response.dimension_headers[1].name = "dimension2"
        mock_response.metric_headers[0].name = "metric1"
        mock_response.metric_headers[1].name = "metric2"
        mock_response.rows[0].dimension_values[0].value = "dvalue1"
        mock_response.rows[0].dimension_values[1].value = "dvalue2"
        mock_response.rows[0].metric_values[0].value = "mvalue1"
        mock_response.rows[0].metric_values[1].value = "mvalue2"

        report = tool._generate_report(mock_response)
        expected_report = "dimension1 dimension2 metric1 metric2 \ndvalue1 dvalue2 mvalue1 mvalue2 \n"
        self.assertEqual(report, expected_report)


    def test_generate_filename(self):
        tool = GoogleAnalyticsReportTool()
        filename = tool._generate_filename(['dimension1'], ['metric1'], ['report.txt'])
        expected_filename = "dimension1metric1.txt"
        self.assertEqual(filename, expected_filename)

    @patch("superagi.tools.marketplace_tools.googleanalytics.google_analytics_report_tool.yaml")
    @patch("builtins.open")
    def test_get_dimensions_and_metrics(self, mock_open, mock_yaml):
        tool = GoogleAnalyticsReportTool()
        mock_yaml.load.return_value = {'GOOGLE_ANALYTICS_VARIABLES': [{'Dimension': '1', 'Metric': '2'}]}
        result = tool.get_dimensions_and_metrics()
        expected_result = [['1', '2']]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()