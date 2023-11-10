import unittest
from unittest.mock import patch

from google_serp_search_toolkit import GoogleSerpToolkit

class TestGoogleSerpToolkit(unittest.TestCase):

    def setUp(self):
        self.toolkit = GoogleSerpToolkit()

    def test_get_tools(self):
        tools = self.toolkit.get_tools()
        tool_names = [tool.name for tool in tools]

        self.assertIn('Google SERP Search', tool_names)

    def test_get_env_keys(self):
        env_keys = self.toolkit.get_env_keys()
        key_names = [key.key for key in env_keys]

        self.assertIn('SERP_API_KEY', key_names)

if __name__ == '__main__':
    unittest.main()