from urllib.parse import parse_qs
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaIoBaseDownload
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeHelper:
    def __init__(self, youtube_key) -> None:
        self.youtube_key = youtube_key
        
        # Client building
        api_service_name = "youtube"
        api_version = "v3"

        self.youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=youtube_key)

    def youtube_request_video(self, part: str = None, maxResults: int = 25, 
                        id: str = None):
        request = self.youtube_client.videos().list(
                part=part,
                maxResults=maxResults,
                id=id,
        )
        response = request.execute()
        return response
    
    def youtube_request_video_captions(self, videoId: str = None):
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        final_captions = []
        for line in transcript:
            final_captions.append(line['text'])

        return final_captions

    def get_video_id(self, video_link):
        return list(parse_qs(video_link).values())[0][0]
