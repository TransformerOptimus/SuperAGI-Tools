from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper


class YoutubeFetchVideoSchema(BaseModel):
    video_links: list = Field(..., description="List of links of videos to be fetched, can be one but not None")


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
            video_link: link to the video that is to be fetched

        Returns:
            List:Video info, if fetched successfully, otherwise an error message
        """
        try:
            if video_links is None:
                raise ValueError("At least one argument must be provided")

            youtube_key = self.get_tool_config('YOUTUBE_KEY')
            youtube_helper = YoutubeHelper(youtube_key)

            # Getting the video ids
            video_ids = ""
            for link in video_links:
                video_ids += youtube_helper.get_video_id(link) + ","

            # Making the request
            part="id,snippet,contentDetails,fileDetails,liveStreamingDetails,localizations,player,processingDetails,recordingDetails,statistics,status,suggestions,topicDetails",
            request = youtube_helper.youtube_request(part, video_ids)
            video_info = request['items']

            print("Video info fetched successfully")
            return video_info
        except Exception as err:
            print("Error occured while fetching video")
            return err