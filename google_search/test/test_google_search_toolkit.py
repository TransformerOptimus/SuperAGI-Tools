import unittest

from google_search.google_search import GoogleSearchTool
from google_search.google_search_toolkit import GoogleSearchToolkit


class TestGoogleSearchToolkit(unittest.TestCase):

    def setUp(self):
        """
        Set up the test fixture.

        This method is called before each test method is executed to prepare the test environment.

        Returns:
            None
        """
        self.toolkit = GoogleSearchToolkit()

    def test_get_tools(self):
        """
        Test the `get_tools` method of the `GoogleSearchToolkit` class.

        It should return a list of tools, containing one instance of `GoogleSearchTool`.

        Returns:
            None
        """

        tools = self.toolkit.get_tools()
        self.assertEqual(1, len(tools))
        self.assertIsInstance(tools[0], GoogleSearchTool)

    def test_get_env_keys(self):
        """
        Test the `get_env_keys` method of the `GoogleSearchToolkit` class.

        It should return an empty list of environment keys.

        Returns:
            None
        """
        env_keys = self.toolkit.get_env_keys()
        self.assertEqual(0, len(env_keys))
