# NewsAPI Toolkit for SuperAGI

The NewsAPI Toolkit is a tool for SuperAGI that allows you to retrieve news articles from the NewsAPI. This README provides instructions on how to set up and use the toolkit.

## Prerequisites

Before using the NewsAPI Toolkit, make sure you have the following prerequisites:

1.  **NewsAPI API Key:** You will need a valid API key from NewsAPI to access their services. You can obtain an API key by signing up on their website.

2.  **Python:** Ensure you have Python installed on your system. This toolkit is designed to work with Python 3.

## Setup

Follow these steps to set up and use the NewsAPI Toolkit:

1.  **Installation:**
-  Clone this repository to your local machine.
-  Install the required Python packages using `pip`:
      ```
      pip install -r requirements.txt
      ```


2.  **API Key Configuration:**

-  Open the `config.py` file and replace `YOUR_NEWSAPI_API_KEY` with your NewsAPI API key.
3.  **Run the Toolkit:**

-  Execute the toolkit by running the script:

      ```
      python newsapi_articles_tool.py
      ```

4.  **Toolkit Usage:**

-  The toolkit allows you to search for news articles by keywords, sources, language, and maximum results.
-  You can use the `GetNewsArticlesInput` parameters to customize your query.

## Example Usage

Here's an example of using the toolkit:

```python
from newsapi_articles_tool import GetNewsArticlesTool, GetNewsArticlesInput

# Create a tool instance
news_tool = GetNewsArticlesTool()

# Define sample input parameters
tool_input = GetNewsArticlesInput(keywords="India",sources="bbc-news", max_results=10, language="en")

# Execute the tool with the input
result = news_tool._execute(**tool_input.dict())

# Access the retrieved news articles
articles = result.get("articles")
print(articles)
```
