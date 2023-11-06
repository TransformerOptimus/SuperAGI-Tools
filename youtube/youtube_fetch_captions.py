from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from helper.youtube_helper import YoutubeHelper
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeFetchCaptionsSchema(BaseModel):
    video_link: str = Field(..., description='''Link of video whose captions 
                            are to be fetched''')


class YoutubeFetchCaptionsTool(BaseTool):
    """
    Youtube fetch video captions Tool
    """
    name: str = "Youtube fetch video captions Tool"
    args_schema: Type[YoutubeFetchCaptionsSchema] = YoutubeFetchCaptionsSchema
    description: str = "Tool for fetching the captions of a youtube video"

    def _execute(self, video_link: str = None):
        """
        Execute the Youtube fetch video captions tool

        Args:
            video_link: Link of video whose captions are to be fetched

        Returns:
            List: Video transcript list with time stamp (text, time), if fetched 
            successfully, otherwise an error message
        """
        if not video_link:
            raise ValueError("At least one argument must be provided")

        youtube_key = self.get_tool_config('YOUTUBE_KEY')
        youtube_helper = YoutubeHelper(youtube_key)

        # Getting the video id
        video_id = youtube_helper.get_video_id(video_link)

        # Getting the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        final_captions = []
        for line in transcript:
            final_captions.append((line['text'], line['start']))

        print("Videos' transcript fetched successfully")
        return final_captions
