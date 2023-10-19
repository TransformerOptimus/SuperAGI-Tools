import unittest
import json
from os import getcwd
import sys
module_path = getcwd().replace("tests","")
sys.path.append(module_path)
from get_news_articles_tool import GetNewsArticlesTool, GetNewsArticlesInput


class GetNewsArticlesToolTestCase(unittest.TestCase):
    results = {}

    def setUp(self):
        self.tool = GetNewsArticlesTool()

    def test_tool_name(self):
        # Your test logic here
        test_result = self.tool.name
        self.results["test_tool_name"] = test_result

    def test_tool_args_schema(self):
        # Your test logic here
        test_result = self.tool.args_schema.__name__
        self.results["test_tool_args_schema"] = test_result

    def test_tool_description(self):
        # Your test logic here
        test_result = self.tool.description
        self.results["test_tool_description"] = test_result

    def test_successful_retrieval(self):
        # Create a tool instance
        news_tool = GetNewsArticlesTool()

        # Define sample input parameters for successful retrieval
        tool_input = GetNewsArticlesInput(keywords="India",sources="bbc-news", max_results=10, language="en")

        # Execute the tool with the tool_input
        result = news_tool._execute(**tool_input.dict())

        # Capture the response JSON
        response_json = result

        # Include the response JSON in the test results
        self.results["test_successful_retrieval"] = {
            "status": "ok",
            "totalResults": 6,  
            "articles": response_json,
        }


    def test_no_results(self):
        # Create a tool instance
        news_tool = GetNewsArticlesTool()

        # Define sample input parameters for a query with no results
        tool_input = GetNewsArticlesInput(keywords="Zzzzzzzzzzz", max_results=10)

        # Execute the tool with the tool_input
        result = news_tool._execute(**tool_input.dict())

        # Ensure the response is empty
        articles = result.get("articles")

        if not articles:
            test_result = "Passed"
        else:
            test_result = "Failed"

        self.results["test_no_results"] = test_result

    def test_invalid_input(self):
        # Create a tool instance
        news_tool = GetNewsArticlesTool()

        # Define sample input parameters with invalid values
        tool_input = GetNewsArticlesInput(keywords=12345, max_results=-5)

        try:
            news_tool._execute(**tool_input.dict())
            test_result = "Failed"
        except ValueError:
            test_result = "Passed"

        self.results["test_invalid_input"] = test_result

    @classmethod
    def tearDownClass(cls):
        # Serialize and save the results as JSON
        with open('test_results.json', 'w') as f:
            json.dump(cls.results, f, indent=4)

if __name__ == '__main__':
    unittest.main()
