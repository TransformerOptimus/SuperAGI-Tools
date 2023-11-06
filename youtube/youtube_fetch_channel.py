from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper


class YoutubeFetchChannelSchema(BaseModel):
    channel_id: str = Field(..., description="ID of the channel whose info is to be fetched")
    username: str = Field(..., description="Username of the channel whose info is to be fetched")
    content_owner_id: str = Field(..., description="Content ID of the channel whose info is to be fetched")

class YoutubeFetchChannelTool(BaseTool):
    """
    Youtube fetch channel Tool
    """
    name: str = "Youtube fetch channel Tool"
    args_schema: Type[YoutubeFetchChannelSchema] = YoutubeFetchChannelSchema
    description: str = "Tool for fetching all information of a youtube channel"

    def _execute(self, channel_id: str = None, username: str = None, content_owner_id: str = None):
        """
        Execute the Youtube fetch channel tool

        Args:
            channel_id: ID of the channel that is to be fetched
            username: Username of the channel that is to be fetched
            content_owner_id: Content ID of the channel that is to be fetched

        Returns:
            List: Channel info, if fetched successfully, otherwise an error message
        """

        # Checking for args
        args = [content_owner_id, channel_id, username]
        request_id = None
        for arg in args:
            if arg is not None:
                request_id = arg
                break
        if request_id is None:
            raise ValueError("At least one argument must be provided")

        youtube_key = self.get_tool_config('YOUTUBE_KEY')
        youtube_helper = YoutubeHelper(youtube_key)

        # Making the request
        part="id,snippet,brandingSettings,localizations,statistics,status,topicDetails"
        request = youtube_helper.youtube_client.channels().list(
            part=part,
            id=request_id,
        ).execute()
        channel_info = request['items']

        print("Channel info fetched successfully")
        return channel_info
