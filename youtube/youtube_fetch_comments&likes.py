from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class GreetingsInput(BaseModel):
    greetings: str = Field(..., description="Link of the video to be fetched")


class GreetingsTool(BaseTool):
    """
    Greetings Tool
    """
    name: str = "YouTube video fetch Tool"
    args_schema: Type[BaseModel] = GreetingsInput
    description: str = "Tool for fetching "

    def _execute(self, greetings: str = None):
        from_name = self.get_tool_config('FROM')
        greetings_str = greetings + "\n" + from_name
        return greetings_str