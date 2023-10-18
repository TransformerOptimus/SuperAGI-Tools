from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class GreetingsInput(BaseModel):
    greetings: str = Field(..., description="Link of the video to be fetched")


class YoutubefetchvideoTool(BaseTool):
    """
    Youtube fetch video Tool
    """
    name: str = "YoutubefetchvideoTool"
    args_schema: Type[BaseModel] = GreetingsInput
    description: str = "Tool for fetching all information of a youtube video"

    def _execute(self, greetings: str = None):
        from_name = self.get_tool_config('YOUTUBE_KEY')
        greetings_str = greetings + "\n" + from_name
        return greetings_str