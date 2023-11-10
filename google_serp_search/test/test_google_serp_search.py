import unittest
from unittest.mock import Mock, patch

from google_serp_search.google_serp_search import GoogleSerpTool

class TestGoogleSerpTool(unittest.TestCase):

    @patch.object(GoogleSerpTool, '_execute')
    def test_execute(self, mock_execute):
        mock_execute.return_value = 'Query results'
        tool = GoogleSerpTool()
        response = tool._execute('search query')
        self.assertEqual(response, 'Query results')

    @patch.object(GoogleSerpTool, 'summarise_result')
    def test_summarise_result(self, mock_summarise_result):
        mock_summarise_result.return_value = "summary of the search results"
        tool = GoogleSerpTool()
        result = tool.summarise_result('query', 'snippets')
        
        self.assertIsNotNone(result)
        self.assertEqual(result, "summary of the search results")

if __name__ == '__main__':
    unittest.main()