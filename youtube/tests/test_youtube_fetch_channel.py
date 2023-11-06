import unittest
from unittest.mock import Mock, patch

from ..youtube_fetch_channel import YoutubeFetchChannelTool
from ..helper.youtube_helper import YoutubeHelper

class TestYoutubeFetchChannelTool(unittest.TestCase):
    @patch('helper.youtube_helper.YoutubeHelper')
    def test_execute_with_valid_channel_id(self, mock_youtube_helper):
        # Create an instance of YoutubeFetchChannelTool
        channel_tool = YoutubeFetchChannelTool()

        # Mock the YoutubeHelper instance
        mock_helper = YoutubeFetchChannelTool()
        mock_helper.youtube_client.channels().list().execute.return_value = {
            'items': [
                {
                    'id': 'channel_id1',
                    'snippet': {
                        'title': 'Channel 1',
                        'description': 'Description of Channel 1'
                    },
                    'statistics': {
                        'subscriberCount': '1000',
                        'viewCount': '100000'
                    }
                }
            ]
        }
        mock_youtube_helper.return_value = mock_helper

        # Set up the input channel_id
        channel_id = "channel_id1"

        # Call the _execute method
        result = channel_tool._execute(channel_id)

        # Check if the method returns the expected channel information
        expected_result = [
            {
                'id': 'channel_id1',
                'snippet': {
                    'title': 'Channel 1',
                    'description': 'Description of Channel 1'
                },
                'statistics': {
                    'subscriberCount': '1000',
                    'viewCount': '100000'
                }
            }
        ]
        self.assertEqual(result, expected_result)

    def test_execute_with_missing_args(self):
        # Create an instance of YoutubeFetchChannelTool
        channel_tool = YoutubeFetchChannelTool()

        # Call the _execute method without providing any arguments
        with self.assertRaises(ValueError) as context:
            channel_tool._execute()

        # Check if the method raises a ValueError for missing arguments
        self.assertEqual(str(context.exception), "At least one argument must be provided")

if __name__ == '__main__':
    unittest.main()
