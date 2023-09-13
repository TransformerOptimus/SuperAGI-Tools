import unittest
import pytest
from unittest.mock import Mock, patch
from apollo_search import ApolloSearchTool


class TestApolloSearchTool(unittest.TestCase):

    @patch('apollo_search.ApolloSearchTool._execute')
    def test_execute(self):
        toolkit = ApolloSearchTool()
        result = toolkit._execute(["CEO"], 1, 25, [100,200], "New York", "apple.com")
        self.assertIsNotNone(result)

    @patch('apollo_search.ApolloSearchTool.apollo_search_results')
    def test_apollo_search_results(self):
        toolkit = ApolloSearchTool()
        result = toolkit.apollo_search_results(1, 25, ["CEO"], [100,200], "New York", "apple.com")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()