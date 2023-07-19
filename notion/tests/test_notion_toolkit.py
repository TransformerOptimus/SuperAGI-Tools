import pytest
from unittest.mock import patch, Mock

from ..notion_create_page import NotionCreatePageTool
from ..notion_fetch_page import NotionfetchPageTool
from ..notion_toolkit import NotionToolkit

def test_notion_toolkit_properties():
    toolkit = NotionToolkit()
    assert toolkit.name == "Notion Toolkit"
    assert toolkit.description == "Toolkit containing tools for performing notion operations"

def test_get_tools():
    toolkit = NotionToolkit()
    tools = toolkit.get_tools()
    assert isinstance(tools, list)
    assert len(tools) == 2
    print(type(tools[0]))
    print(type(NotionCreatePageTool))
    assert isinstance(tools[0], NotionCreatePageTool)
    assert isinstance(tools[1], NotionfetchPageTool)

def test_get_env_keys():
    toolkit = NotionToolkit()
    keys = toolkit.get_env_keys()
    assert isinstance(keys, list)
    assert len(keys) == 2
    assert keys == ["NOTION_TOKEN", "NOTION_DATABASE_ID"]