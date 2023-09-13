import unittest
from unittest.mock import Mock, patch

from google_search.google_search import GoogleSearchTool, GoogleSearchSchema

class TestGoogleSearchTool(unittest.TestCase):

    @patch.object(GoogleSearchTool, '_execute')
    def test_execute(self, mock_execute):
        mock_execute.return_value = [{'title': 'title', 'body': 'body', 'links': 'links'}]
        tool = GoogleSearchTool()
        result = tool._execute('hello world')
        self.assertIsNotNone(result)
        self.assertEqual(result, [{'title': 'title', 'body': 'body', 'links': 'links'}])

    @patch.object(GoogleSearchTool, 'summarise_result')
    def test_summarise_result(self, mock_summarise_result):
        mock_summarise_result.return_value = "summary of the search results"
        tool = GoogleSearchTool()
        result = tool.summarise_result('query', 'snippets')
        
        self.assertIsNotNone(result)
        self.assertEqual(result, "summary of the search results")

if __name__ == '__main__':
    unittest.main()
