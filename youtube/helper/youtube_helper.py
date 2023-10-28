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

    def get_video_id(self, video_link):
        return list(parse_qs(video_link).values())[0][0]
