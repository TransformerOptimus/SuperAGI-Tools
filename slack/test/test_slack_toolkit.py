import unittest
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from slack.send_message import SlackMessageTool
from superagi.types.key_type import ToolConfigKeyType
from slack_toolkit import SlackToolkit 

class TestSlackToolkit(unittest.TestCase):

    def setUp(self):
        self.slack_toolkit = SlackToolkit()

    def test_name(self):
        self.assertEqual(self.slack_toolkit.name, "Slack Toolkit")

    def test_description(self):
        self.assertEqual(self.slack_toolkit.description, "Toolkit containing tools for Slack integration")

    def test_get_tools(self):
        tools = self.slack_toolkit.get_tools()
        self.assertIsInstance(tools, list)
        self.assertEqual(len(tools), 1)
        self.assertIsInstance(tools[0], SlackMessageTool)

    def test_get_env_keys(self):
        env_keys = self.slack_toolkit.get_env_keys()
        self.assertIsInstance(env_keys, list)
        self.assertEqual(len(env_keys), 1)

        self.assertEqual(env_keys[0].key, "SLACK_BOT_TOKEN")
        self.assertEqual(env_keys[0].key_type, ToolConfigKeyType.STRING)
        self.assertTrue(env_keys[0].is_required)
        self.assertTrue(env_keys[0].is_secret)

if __name__ == "__main__":
    unittest.main()