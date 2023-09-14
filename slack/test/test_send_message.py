import unittest
from unittest.mock import patch, Mock
from send_message import SlackMessageTool, SlackMessageSchema

class TestSlackMessageTool(unittest.TestCase):

    def setUp(self):
        self.slack_tool = SlackMessageTool()

    def test_description(self):
        self.assertEqual(self.slack_tool.description, "Send text message in Slack")

    def test_name(self):
        self.assertEqual(self.slack_tool.name, "SendSlackMessage")

    def test_args_schema(self):
        self.assertIs(self.slack_tool.args_schema, SlackMessageSchema)

    @patch("SlackMessageTool.WebClient")
    def test_build_slack_web_client(self, mock_web_client):
        self.slack_tool.build_slack_web_client()
        mock_web_client.assert_called_once()

    @patch("SlackMessageTool.WebClient")
    def test_execute(self, mock_web_client):
        mock_web_client.chat_postMessage.return_value = {"ok": True}
        response = self.slack_tool._execute("test_channel", "test_message")
        self.assertEqual(response, "Message sent to test_channel Successfully")

        mock_web_client.chat_postMessage.return_value = {"ok": False}
        response = self.slack_tool._execute("test_channel", "test_message")
        self.assertEqual(response, "Message sending failed!")

if __name__ == "__main__":
    unittest.main()