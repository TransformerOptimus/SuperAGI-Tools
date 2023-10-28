from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper


class YoutubeFetchVideoSchema(BaseModel):
    video_links: list = Field(..., description='''List of links to videos to be 
                              fetched. Can be one but not None''')


class YoutubeFetchVideoTool(BaseTool):
    """
    Youtube fetch video Tool
    """
    name: str = "Youtube fetch video Tool"
    args_schema: Type[YoutubeFetchVideoSchema] = YoutubeFetchVideoSchema
    description: str = "Tool for fetching all information of a youtube video"

    def _execute(self, video_links: list = []):
        """
        Execute the Youtube fetch video tool

        Args:
            video_links: List of links of videos to be fetched. Can fetch info 
                         for multiple videos

        Returns:
            List: Video info, if fetched successfully, otherwise an error message
        """
        if not video_links:
            raise ValueError("At least one argument must be provided")

        youtube_key = self.get_tool_config('YOUTUBE_KEY')
        youtube_helper = YoutubeHelper(youtube_key)

        # Getting the video ids
        video_ids = ""
        for link in video_links:
            video_ids += youtube_helper.get_video_id(link) + ","

        # Making the request
        part='''id,snippet,contentDetails,liveStreamingDetails,
                recordingDetails,statistics,status,topicDetails'''
        request = youtube_helper.youtube_client.videos().list(
                part=part,
                id=video_ids,
        ).execute()
        videos_info = request['items']

        print("Videos' info fetched successfully")
        return videos_info
