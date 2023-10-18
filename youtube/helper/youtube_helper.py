from urllib.parse import parse_qs
import googleapiclient.discovery
import googleapiclient.errors

class YoutubeHelper:
    def __init__(self, youtube_key) -> None:
        self.youtube_key = youtube_key
        
        # Client building
        api_service_name = "youtube"
        api_version = "v3"

        self.youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=youtube_key)

    def get_video_info(self, video_link):
        # Getting video id
        video_id = parse_qs(video_link)["v"][0]

        # Request
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        return response
