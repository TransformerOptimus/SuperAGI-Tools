
import unittest
import pytest
from unittest.mock import Mock, patch
from apollo_toolkit import ApolloToolkit

class TestApolloToolkit(unittest.TestCase):

    @patch('apollo_toolkit.ApolloToolkit.get_tools')
    def test_get_tools(self):
        toolkit = ApolloToolkit()
        result = toolkit.get_tools()
        self.assertIn('ApolloSearchTool', str(result))

    @patch('apollo_toolkit.ApolloToolkit.get_env_keys')
    def test_get_env_keys(self):
        toolkit = ApolloToolkit()
        result = toolkit.get_env_keys()
        self.assertEqual(result[0].key, 'APOLLO_SEARCH_KEY')