import unittest
from unittest.mock import Mock, patch

from ..youtube_fetch_comments import YoutubeFetchCommentsTool
from ..helper.youtube_helper import YoutubeHelper

class TestYoutubeFetchCommentsTool(unittest.TestCase):
    @patch('helper.youtube_helper.YoutubeHelper')
    def test_execute_with_valid_video_link(self, mock_youtube_helper):
        # Create an instance of YoutubeFetchCommentsTool
        comments_tool = YoutubeFetchCommentsTool()

        # Mock the YoutubeHelper instance
        mock_helper = YoutubeFetchCommentsTool()
        mock_helper.get_video_id.return_value = "video_id1"
        mock_helper.youtube_client.commentThreads().list().execute.return_value = {
            'items': [
                {
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'commentId': 'comment_id1',
                                'textOriginal': 'Comment 1'
                            }
                        },
                        'replies': {
                            'comments': [
                                {
                                    'snippet': {
                                        'commentId': 'comment_id2',
                                        'textOriginal': 'Reply 1 to Comment 1'
                                    }
                                }
                            ]
                        }
                    }
                },
                {
                    'snippet': {
                        'topLevelComment': {
                            'snippet': {
                                'commentId': 'comment_id3',
                                'textOriginal': 'Comment 2'
                            }
                        },
                        'replies': {
                            'comments': []
                        }
                    }
                }
            ]
        }
        mock_youtube_helper.return_value = mock_helper

        # Set up the input video link
        video_link = "https://www.youtube.com/watch?v=video_id1"

        # Call the _execute method
        result = comments_tool._execute(video_link, max_comments=2)

        # Check if the method returns the expected comments and replies
        expected_result = [
            {
                'parent_comment': {
                    'commentId': 'comment_id1',
                    'textOriginal': 'Comment 1'
                },
                'replies': [
                    {
                        'commentId': 'comment_id2',
                        'textOriginal': 'Reply 1 to Comment 1'
                    }
                ]
            },
            {
                'parent_comment': {
                    'commentId': 'comment_id3',
                    'textOriginal': 'Comment 2'
                },
                'replies': []
            }
        ]
        self.assertEqual(result, expected_result)

    def test_execute_with_missing_video_link(self):
        # Create an instance of YoutubeFetchCommentsTool
        comments_tool = YoutubeFetchCommentsTool()

        # Call the _execute method without providing a video link
        with self.assertRaises(ValueError) as context:
            comments_tool._execute(None)

        # Check if the method raises a ValueError for missing video link
        self.assertEqual(str(context.exception), "At least one argument must be provided")

if __name__ == '__main__':
    unittest.main()
