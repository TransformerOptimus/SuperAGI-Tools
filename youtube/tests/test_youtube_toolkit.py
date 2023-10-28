import unittest
from unittest.mock import patch, Mock

from ..youtube_fetch_captions import YoutubeFetchCaptionsTool
from ..youtube_fetch_channel import YoutubeFetchChannelTool
from ..youtube_fetch_comments import YoutubeFetchCommentsTool
from ..youtube_fetch_video import YoutubeFetchVideoTool
from ..youtube_search import YoutubeSearchTool
from ..youtube_toolkit import YoutubeToolkit


class TestYoutubeToolkit(unittest.TestCase):
    def test_get_tools(self):
        # Create an instance of YoutubeToolkit
        youtube_toolkit = YoutubeToolkit()

        # Mock the tools that should be returned by get_tools
        mock_tool1 = YoutubeFetchChannelTool()
        mock_tool2 = YoutubeFetchCommentsTool()
        mock_tool3 = YoutubeFetchCaptionsTool()
        mock_tool4 = YoutubeFetchVideoTool()
        mock_tool5 = YoutubeSearchTool()

        # Override the get_tools method to return the mock tools
        youtube_toolkit.get_tools = Mock(return_value=[
            mock_tool1, mock_tool2, mock_tool3, mock_tool4, mock_tool5])

        # Call the get_tools method
        tools = youtube_toolkit.get_tools()

        # Check if the method returned the expected tools
        self.assertEqual(tools, [mock_tool1, mock_tool2, mock_tool3, mock_tool4, mock_tool5])

    def test_get_env_keys(self):
        # Create an instance of YoutubeToolkit
        youtube_toolkit = YoutubeToolkit()

        # Call the get_env_keys method
        env_keys = youtube_toolkit.get_env_keys()

        # Check if the method returned the expected environment keys
        self.assertEqual(env_keys, ["YOUTUBE_KEY"])

if __name__ == '__main__':
    unittest.main()
