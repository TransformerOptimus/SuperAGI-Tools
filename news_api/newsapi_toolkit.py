from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool
from typing import List
from get_news_articles_tool import GetNewsArticlesTool

class NewsAPIToolkit(BaseToolkit, ABC):
    name: str = "NewsAPI Toolkit"
    description: str = "NewsAPI Toolkit contains tools for accessing news articles"

    def get_tools(self) -> List[BaseTool]:
        return [GetNewsArticlesTool()]

    def get_env_keys(self) -> List[str]:
        return []
