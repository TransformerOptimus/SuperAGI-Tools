import unittest
from unittest.mock import Mock, patch
from youtube_transcript_api import Transcript, TranscriptSegment

from ..youtube_fetch_captions import YoutubeFetchCaptionsTool
from ..helper.youtube_helper import YoutubeHelper

class TestYoutubeFetchCaptionsTool(unittest.TestCase):
    @patch('helper.youtube_helper.YoutubeHelper')
    @patch('youtube_transcript_api.YouTubeTranscriptApi')
    def test_execute_with_valid_video_link(self, mock_youtube_helper, mock_transcript_api):
        # Create an instance of YoutubeFetchCaptionsTool
        captions_tool = YoutubeFetchCaptionsTool()

        # Mock the YoutubeHelper instance
        mock_helper = Mock()
        mock_helper.get_video_id.return_value = "video_id1"
        mock_youtube_helper.return_value = mock_helper

        # Mock the Transcript returned by YouTubeTranscriptApi
        mock_transcript = Transcript([TranscriptSegment("Caption 1", 0), TranscriptSegment("Caption 2", 10)])
        mock_transcript_api.get_transcript.return_value = mock_transcript

        # Set up the input video link
        video_link = "https://www.youtube.com/watch?v=video_id1"

        # Call the _execute method
        result = captions_tool._execute(video_link)

        # Check if the method returns the expected transcript
        expected_result = [("Caption 1", 0), ("Caption 2", 10)]
        self.assertEqual(result, expected_result)

    def test_execute_with_missing_video_link(self):
        # Create an instance of YoutubeFetchCaptionsTool
        captions_tool = YoutubeFetchCaptionsTool()

        # Call the _execute method without providing a video link
        with self.assertRaises(ValueError) as context:
            captions_tool._execute(None)

        # Check if the method raises a ValueError for missing video link
        self.assertEqual(str(context.exception), "At least one argument must be provided")

if __name__ == '__main__':
    unittest.main()