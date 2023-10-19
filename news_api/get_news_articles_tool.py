from json import dump
from typing import Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
import requests
from config import NEWSAPI_API_KEY

class GetNewsArticlesInput(BaseModel):
    keywords: str = Field(..., description="Keywords to search for news articles.")
    sources: str = Field("", description="Optional news sources.")
    language: str = Field("en", description="Language of the articles.")
    max_results: int = Field(5, description="The maximum number of articles to retrieve.")

class GetNewsArticlesTool(BaseTool):
    '''
        NewsApI Tool   
    '''
    name: str = "Get News Articles"
    args_schema: Type[BaseModel] = GetNewsArticlesInput
    description: str = "Retrieves news articles from NewsAPI."

    def _execute(self, keywords, max_results=5, sources="", language="en") -> dict:
        if not isinstance(keywords, str) or not isinstance(sources, str) or not isinstance(language, str) or not isinstance(max_results, int) or max_results < 1:
            raise ValueError("Invalid input values. Please provide valid input parameters.")
        
        url = f"https://newsapi.org/v2/everything?q={keywords}&sources={sources}&language={language}&apiKey={NEWSAPI_API_KEY}"
        
        response = requests.get(url)
        print("API URL:", url)
        print("API Response:", response.json())

        
        if response.status_code == 200:
            articles = response.json().get("articles")
            return {"articles": articles[:max_results]}
        else:
            return {"error": "Unable to retrieve news articles."}

