import unittest
from unittest.mock import Mock
from superagi.tools.base_tool import BaseTool, ToolConfiguration
from superagi.tools.marketplace_tools.googleanalytics.google_analytics_toolkit import GoogleAnalyticsToolkit

class TestGoogleAnalyticsToolkit(unittest.TestCase):
    def setUp(self):
        self.toolkit = GoogleAnalyticsToolkit()

    def test_name(self):
        self.assertEqual(self.toolkit.name, "Google Analytics Toolkit")
     
    def test_description(self):
        self.assertEqual(self.toolkit.description, "Google Analytics Toolkit returns google analytics reports requested by the user")
    
    def test_get_tools(self):
        tools = self.toolkit.get_tools()
        self.assertTrue(any(isinstance(tool, BaseTool) for tool in tools))

    def test_get_env_keys(self):
        env_keys = self.toolkit.get_env_keys()
        self.assertTrue(all(isinstance(env_key, ToolConfiguration) for env_key in env_keys))
        
        # check required values are present in env_keys
        keys = [k.key for k in env_keys]
        self.assertIn("PROPERTY_ID", keys)
        self.assertIn("GOOGLE_CREDENTIALS_FILE", keys)

        
if __name__ == "__main__":
    unittest.main()