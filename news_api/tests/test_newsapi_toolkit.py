import unittest
import sys
from os import getcwd

module_path = getcwd().replace("tests","")
sys.path.append(module_path)
print(module_path)

from newsapi_toolkit import NewsAPIToolkit
from get_news_articles_tool import GetNewsArticlesTool

class NewsAPIToolkitTests(unittest.TestCase):

    def setUp(self):
        self.toolkit = NewsAPIToolkit()

    def test_get_tools_returns_list_of_tools(self):
        tools = self.toolkit.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(all(isinstance(tool, GetNewsArticlesTool) for tool in tools))

    def test_get_env_keys_returns_list_of_strings(self):
        env_keys = self.toolkit.get_env_keys()
        self.assertIsInstance(env_keys, list)
        self.assertTrue(all(isinstance(key, str) for key in env_keys))

    def test_toolkit_has_name_and_description(self):
        self.assertEqual(self.toolkit.name, "NewsAPI Toolkit")
        self.assertEqual(self.toolkit.description, "NewsAPI Toolkit contains tools for accessing news articles")

if __name__ == '__main__':
    unittest.main()
