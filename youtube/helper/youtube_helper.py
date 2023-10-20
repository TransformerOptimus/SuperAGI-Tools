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

    def youtube_request(self, part: str = None, maxResults: int = 25, id: str = None, q: str = None):
        try:
            request = self.youtube_client.channels().list(
                    part=part,
                    maxResults=maxResults,
                    id=id,
                    q=q
            )
            response = request.execute()
            return response
        except Exception as err:
            return err

    def get_video_id(self, video_link):
        return parse_qs(video_link)["v"][0]
