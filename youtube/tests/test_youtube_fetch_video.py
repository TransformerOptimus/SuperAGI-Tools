import unittest
from unittest.mock import Mock, patch

from ..youtube_fetch_video import YoutubeFetchVideoTool
from ..helper.youtube_helper import YoutubeHelper

class TestYoutubeFetchVideoTool(unittest.TestCase):
    @patch('helper.youtube_helper.YoutubeHelper')
    def test_execute_with_valid_links(self, mock_youtube_helper):
        # Create an instance of YoutubeFetchVideoTool
        video_tool = YoutubeFetchVideoTool()

        # Mock the YoutubeHelper instance
        mock_helper = YoutubeFetchVideoTool()
        mock_helper.get_video_id.return_value = "video_id1"
        mock_helper.youtube_client.videos().list().execute.return_value = {
            'items': [
                {'videoId': 'video_id1', 'title': 'Video 1'},
                {'videoId': 'video_id2', 'title': 'Video 2'}
            ]
        }
        mock_youtube_helper.return_value = mock_helper

        # Set up the input video links
        video_links = ["https://www.youtube.com/watch?v=video_id1", "https://www.youtube.com/watch?v=video_id2"]

        # Call the _execute method
        result = video_tool._execute(video_links)

        # Check if the method returns the expected video information
        expected_result = [
            {'videoId': 'video_id1', 'title': 'Video 1'},
            {'videoId': 'video_id2', 'title': 'Video 2'}
        ]
        self.assertEqual(result, expected_result)

    def test_execute_with_missing_links(self):
        # Create an instance of YoutubeFetchVideoTool
        video_tool = YoutubeFetchVideoTool()

        # Call the _execute method without providing video links
        with self.assertRaises(ValueError) as context:
            video_tool._execute([])

        # Check if the method raises a ValueError for missing video links
        self.assertEqual(str(context.exception), "At least one argument must be provided")

if __name__ == '__main__':
    unittest.main()
