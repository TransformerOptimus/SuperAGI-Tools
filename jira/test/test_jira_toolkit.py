import unittest
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from jira.create_issue import CreateIssueTool
from jira.edit_issue import EditIssueTool
from jira.get_projects import GetProjectsTool
from jira.search_issues import SearchJiraTool
from superagi.types.key_type import ToolConfigKeyType
from jira_toolkit import JiraToolkit 

class TestJiraToolkit(unittest.TestCase):

    def setUp(self):
        self.jira_toolkit = JiraToolkit()

    def test_name(self):
        self.assertEqual(self.jira_toolkit.name, "Jira Toolkit")

    def test_description(self):
        self.assertEqual(self.jira_toolkit.description, "Toolkit containing tools for Jira integration")

    def test_get_tools(self):
        tools = self.jira_toolkit.get_tools()
        self.assertIsInstance(tools, list)
        self.assertEqual(len(tools), 4)
        self.assertIsInstance(tools[0], CreateIssueTool)
        self.assertIsInstance(tools[1], EditIssueTool)
        self.assertIsInstance(tools[2], GetProjectsTool)
        self.assertIsInstance(tools[3], SearchJiraTool)

    def test_get_env_keys(self):
        env_keys = self.jira_toolkit.get_env_keys()
        self.assertIsInstance(env_keys, list)
        self.assertEqual(len(env_keys), 3)

        self.assertEqual(env_keys[0].key, "JIRA_INSTANCE_URL")
        self.assertEqual(env_keys[0].key_type, ToolConfigKeyType.STRING)
        self.assertTrue(env_keys[0].is_required)
        self.assertFalse(env_keys[0].is_secret)

        self.assertEqual(env_keys[1].key, "JIRA_USERNAME")
        self.assertEqual(env_keys[1].key_type, ToolConfigKeyType.STRING)
        self.assertTrue(env_keys[1].is_required)
        self.assertFalse(env_keys[1].is_secret)

        self.assertEqual(env_keys[2].key, "JIRA_API_TOKEN")
        self.assertEqual(env_keys[2].key_type, ToolConfigKeyType.STRING)
        self.assertTrue(env_keys[2].is_required)
        self.assertTrue(env_keys[2].is_secret)

if __name__ == "__main__":
    unittest.main()