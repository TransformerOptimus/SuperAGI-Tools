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

    def _execute(self, video_link: str = None, max_comments: int = 20):
        """
        Execute the Youtube fetch comments tool

        Args:
            video_link: link to the video under which comments are to be fetched

        Returns:
            List: Comments under video along with replies, if fetched successfully, otherwise error message
        """

        youtube_key = self.get_tool_config('YOUTUBE_KEY')
        youtube_helper = YoutubeHelper(youtube_key)

        # Getting the video id
        video_id = youtube_helper.get_video_id(video_link)

        # Making the request
        part = "snippet,replies"
        request = youtube_helper.youtube_client.commentThreads().list(
            part=part,
            maxResults=max_comments,
            videoId=video_id,
        ).execute()

        # Formatting the response
        comments_list = []
        for comment in request['items']:
            parent_comment = comment['snippet']['topLevelComment']['snippet']

            comment_replies = []
            if 'replies' in comment:
                for reply in comment['replies']['comments']:
                    comment_replies.append(reply['snippet'])

            comment_and_replies = {
                'parent_comment':parent_comment,
                'replies':comment_replies
            }
            comments_list.append(comment_and_replies)

        print("Comments fetched successfully")
        return comments_list
