from urllib.parse import parse_qs
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper

class YoutubeSearchSchema(BaseModel):
    query: str = Field(..., description="Search query for youtube search.")


class YoutubeSearchTool(BaseTool):
    """
    Youtube fetch comments tool
    """
    name: str = "YouTube video comments fetch Tool"
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
        try:
            if query is None:
                raise ValueError("At least one argument must be provided")
            
            youtube_key = self.get_tool_config('YOUTUBE_KEY')
            youtube_helper = YoutubeHelper(youtube_key)

            # Making the request
            part = "snippit"
            request = youtube_helper.youtube_request(part=part, q=query)

            results = request['items']
            
            print("Query successful")
            return results
        except Exception as err:
            print("Error fetching search results")
            return err