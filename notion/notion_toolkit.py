from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseToolkit, BaseTool
from notion_create_page import NotionCreatePageTool
from notion_fetch_page import NotionfetchPageTool

class NotionToolkit(BaseToolkit, ABC):
    name: str = "Notion Toolkit"
    description: str = "Toolkit containing tools for performing notion operations"

    def get_tools(self) -> List[BaseTool]:
        return [NotionCreatePageTool(),NotionfetchPageTool()]

    def get_env_keys(self) -> List[str]:
        return ["NOTION_TOKEN","NOTION_DATABASE_ID"]
