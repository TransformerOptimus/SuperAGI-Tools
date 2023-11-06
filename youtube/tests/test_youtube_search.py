import unittest
from unittest.mock import Mock, patch

from ..youtube_search import YoutubeSearchTool
from ..helper.youtube_helper import YoutubeHelper

class TestYoutubeSearchTool(unittest.TestCase):
    @patch('helper.youtube_helper.YoutubeHelper')
    def test_execute_with_valid_query(self, mock_youtube_helper):
        # Create an instance of YoutubeSearchTool
        youtube_tool = YoutubeSearchTool()

        # Mock the YoutubeHelper instance
        mock_helper = YoutubeHelper()
        mock_helper.youtube_client.search().list().execute.return_value = {
            'items': [
                {'videoId': 'video_id1', 'title': 'Video 1'},
                {'videoId': 'video_id2', 'title': 'Video 2'}
            ]
        }
        mock_youtube_helper.return_value = mock_helper

        # Set up the input query
        query = "example query"

        # Call the _execute method
        result = youtube_tool._execute(query)

        # Check if the method returns the expected search results
        expected_result = [
            {'videoId': 'video_id1', 'title': 'Video 1'},
            {'videoId': 'video_id2', 'title': 'Video 2'}
        ]
        self.assertEqual(result, expected_result)

    def test_execute_with_missing_query(self):
        # Create an instance of YoutubeSearchTool
        youtube_tool = YoutubeSearchTool()

        # Call the _execute method without providing a query
        with self.assertRaises(ValueError) as context:
            youtube_tool._execute(None)

        # Check if the method raises a ValueError for missing query
        self.assertEqual(str(context.exception), "At least one argument must be provided")

if __name__ == '__main__':
    unittest.main()
