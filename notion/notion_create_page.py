import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.llms.base_llm import BaseLlm
from superagi.tools.base_tool import BaseTool
from superagi.tools.notion.helper.notion_helper import NotionHelper
from superagi.tools.notion.helper.tool_schema_helper import ToolSchemaHelper

class NotionCreatePageSchema(BaseModel):
    content_list:  list = Field( 
        ...,
        description=ToolSchemaHelper.read_tools_schema_description(__file__,"notion_create_page.txt"),
    )
    title: str = Field(
        ...,
        description="Title of the page to be created",
    )                      
    tags: list = Field(
        ...,
        description="list of tags to be added to the page based on the content",
    )

class NotionCreatePageTool(BaseTool):
    """
    Notion Create Page tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    llm: Optional[BaseLlm] = None
    name = "NotionCreatePage"
    description = (
        "A tool for creating a page on Notion."
    )
    args_schema: Type[NotionCreatePageSchema] = NotionCreatePageSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, content_list:list, title:str, tags=None) -> str:
        """
        Execute the Notion Create Page tool.

        Args:
            content: The List of dictionaries containing content,content language and content type.
            title: The name of the page to be created.
            tags: The list of tags for the page.
            database_id: The id of the database in which the page is being created.

        Returns:
            Page created successfully. or error message.
        """
        try:
            Notion_token=self.get_tool_config("NOTION_TOKEN")
            Notion_database_id=self.get_tool_config("NOTION_DATABASE_ID")
            notion_helper=NotionHelper(Notion_token)
            response=notion_helper.create_page(content_list,title,Notion_database_id,tags)
            if isinstance(response, str):
                return response
            elif response.status_code == 200:
                page_data = response.json()
                page_id = page_data["id"]
                return f"Page created successfully. Page ID: {page_id}"
            else:
                return f"Failed to create page. Status code: {response.text}"
        except Exception as err:
            return f"Error: Unable to create page {err}"