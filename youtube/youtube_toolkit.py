from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool
from typing import Type, List

from youtube_fetch_channel import YoutubeFetchChannelTool
from youtube_fetch_comments import YoutubeFetchCommentsTool
from youtube_fetch_captions import YoutubeFetchCaptionsTool
from youtube_fetch_video import YoutubeFetchVideoTool
from youtube_search import YoutubeSearchTool



class GreetingsToolkit(BaseToolkit, ABC):
    name: str = "YouTube Toolkit"
    description: str = "YouTube Tool kit contains all tools related to YouTube"

    def get_tools(self) -> List[BaseTool]:
        return [
            YoutubeFetchChannelTool(),
            YoutubeFetchCommentsTool(),
            YoutubeFetchCaptionsTool(),
            YoutubeFetchVideoTool(),
            YoutubeSearchTool()
        ]

    def get_env_keys(self) -> List[str]:
        return ["YOUTUBE_KEY"]