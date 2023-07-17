import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from superagi.helper.token_counter import TokenCounter
from superagi.tools.notion.helper.notion_helper import NotionHelper



class NotionfetchPageSchema(BaseModel):
    title: str = Field(
        ...,
        description="title of the notion page that has to be fetched",
    )

class NotionfetchPageTool(BaseTool):
    """
    Notion fetch Page tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "NotionfetchPage"
    description = (
        "A tool for fetching notion page."
    )
    args_schema: Type[NotionfetchPageSchema] = NotionfetchPageSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, title:str):
        """
        Execute the Notion fetch Page tool.

        Args:
            title: The title of the notion page that has to be fetched.

        Returns:
            Pages fetched successfully. or No such page exists. or error message.
        """
        try:
            Notion_token=self.get_tool_config("NOTION_TOKEN")
            notion_helper=NotionHelper(Notion_token)
            page_ids=notion_helper.get_ids(title,"page")
            if len(page_ids)==0:
                return "No such page exists."
            try:
                final_result=""
                for i in range(0,len(page_ids)):
                    helper_content_str=notion_helper.get_page_content(page_ids[i])
                    page_content=f"page {i+1}:\n\n{helper_content_str}"
                    final_result+=(f"\n{page_content}")
                    if TokenCounter.count_text_tokens(final_result) > 3000:
                        break

                return f"Pages fetched successfully:{final_result}"
            except Exception as err:
                return f"Error: Unable to fetch page {err}"
        except Exception as err:
            return f"Error: Unable to fetch page {err}"