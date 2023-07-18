import requests
import json

from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from helper.notion_helper import NotionHelper

class NotionCreatePageSchema(BaseModel):
    content_list:  list = Field( 
        ...,
        description='Be very clear about the content_list format.Here is an array of different Notion blocks that you can use in Notion create page API:["paragraph","code","heading_1","heading_2","heading_3","bulleted_list_item","numbered_list_item","to_do","quote","toggle"].content_list should be a list of dictionaries containing content,type of the content and language of the content, example: content_list=[{"type":"based on content, if no such block type exists choose it from the list provided above","content":some text,"language":"which coding language is used"}]. Strictly follow the given example and include the keys type,content and language in the dictionary',
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
            notion_token=self.get_tool_config("NOTION_TOKEN")
            notion_database_id=self.get_tool_config("NOTION_DATABASE_ID")
            notion_helper=NotionHelper(notion_token)
            response=notion_helper.create_page(content_list,title,notion_database_id,tags)
            if response.status_code == 200:
                return f'Page created successfully. Page ID: {response.json()["id"]}'
            else:
                return f"Failed to create page. Status code: {response.text}"
        except Exception as err:
            return f"Error: Unable to create page {err}"