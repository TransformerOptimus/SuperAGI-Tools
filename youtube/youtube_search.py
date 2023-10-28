from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper

class YoutubeSearchSchema(BaseModel):
    query: str = Field(..., description="Search query for youtube search.")


class YoutubeSearchTool(BaseTool):
    """
    Youtube search tool
    """
    name: str = "Youtube search tool"
    args_schema: Type[YoutubeSearchSchema] = YoutubeSearchSchema
    description: str = "Tool for using youtube search"

    def _execute(self, query: str = None):
        """
        Execute the Youtube search tool

        Args:
            query: Search query

        Returns:
            List: Search results, if fetched successfully, otherwise error message
        """

        if query is None:
            raise ValueError("At least one argument must be provided")
        
        youtube_key = self.get_tool_config('YOUTUBE_KEY')
        youtube_helper = YoutubeHelper(youtube_key)

        # Making the request
        part = "snippet"
        # request = youtube_helper.youtube_request(part=part, q=query)
        request = youtube_helper.youtube_client.search().list(
            part=part,
            maxResults=25,
            q=query
        ).execute()
        print("Query successful")

        return request['items']
