import unittest
from unittest.mock import patch, MagicMock
from ..googleanalytics import GoogleAnalyticsReportTool

# assuming these are in a test_google_analytics_report_tool.py file
class TestGoogleAnalyticsReportTool(unittest.TestCase):
    @patch.object(GoogleAnalyticsReportTool, '_execute')
    @patch.object(GoogleAnalyticsReportTool, 'get_tool_config')
    def setUp(self, mock_get_tool_config):
        self.tool = GoogleAnalyticsReportTool()
        self.mock_get_tool_config = mock_get_tool_config   

    def test_execute(self):
        # We could mock the FileManager here but for simplicity we will create specific unit tests for it
        self.tool.resource_manager = MagicMock()
        self.tool._execute("2021-12-01", "2021-12-10", True)
        self.assertTrue(self.tool.resource_manager.write_file.called)

    @patch('os.remove')
    @patch('os.environ')
    def test_set_google_credentials(self, mock_os_environ, mock_os_remove):
        self.tool._set_google_credentials('{"credentials": "abc"}')
        self.assertDictEqual(mock_os_environ, {'GOOGLE_APPLICATION_CREDENTIALS': 'credentials.json'})
        mock_os_remove.assert_called_with('credentials.json')

    @patch('builtins.open')
    def test_get_dimensions_and_metrics(self, mock_open):
        mock_open.return_value.__enter__ = lambda s: s
        mock_open.return_value.__exit__ = MagicMock()
        mock_open.return_value.read.return_value = '{"GOOGLE_ANALYTICS_VARIABLES": [{"Dimension": "dim1", "Metric": "met1"}, {"Dimension": "dim2", "Metric": "met2"}]}'
        result = self.tool.get_dimensions_and_metrics()
        self.assertEqual(result, [["dim1", "met1"], ["dim2", "met2"]])

    def test_generate_report(self):
        mock_response = MagicMock() # Mock response from the google analytics client
        # Setup mock response here
        report = self.tool._generate_report(mock_response)
        # assert report structure/values

    def test_create_run_report_request(self):
        result = self.tool._create_run_report_request('123', ['Dimension'], ['Metric'], "2021-12-01", "2021-12-10")
        # assert results
        pass # Remove and add assertions here

    def test_generate_filename(self):
        filename = self.tool._generate_filename(['Dimension'], ['Metric'], ['report.txt'])
        # assert filename

if __name__ == '__main__':
    unittest.main()
