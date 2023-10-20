from urllib.parse import parse_qs
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper

class YoutubeFetchCommentsSchema(BaseModel):
    video_link: str = Field(..., description="Link of the video from which comments are to be fetched")


class YoutubeFetchCommentsTool(BaseTool):
    """
    Youtube fetch comments tool
    """
    name: str = "YouTube video comments fetch Tool"
    args_schema: Type[YoutubeFetchCommentsSchema] = YoutubeFetchCommentsSchema
    description: str = "Tool for fetching comments under a video"

    def _execute(self, video_link: str = None):
        """
        Execute the Youtube fetch comments tool

        Args:
            video_link: link to the video under which comments are to be fetched

        Returns:
            Comments under video, if fetched successfully, otherwise error message
        """
        try:
            youtube_key = self.get_tool_config('YOUTUBE_KEY')
            youtube_helper = YoutubeHelper(youtube_key)
            
            # Getting the video id
            video_id = youtube_helper.get_video_id(video_link)

            # Making the request
            request = youtube_helper.youtube_client.videos().list(
                part="id,snippet",
                id=video_id
            )
            response = request.execute()
            comments = response['items'][0]
            
            print("Comments fetched successfully")
            return comments
        except Exception as err:
            print("Error fetching comments")
            return err