import pytest
from unittest.mock import patch, MagicMock
from notion_fetch_page import NotionfetchPageTool, NotionfetchPageSchema
from ..helper.notion_helper import NotionHelper

notion_tool = NotionfetchPageTool()


@patch.object(NotionfetchPageTool, 'get_tool_config')
@patch.object(NotionHelper, 'get_page_ids')
def test_no_page_exists(mock_get_page_ids, mock_get_tool_config):
    mock_get_tool_config.return_value = 'TOKEN'
    mock_get_page_ids.return_value = []
    
    result = notion_tool._execute('title')
    
    assert result == "No such page exists."

	
@patch.object(NotionfetchPageTool, 'get_tool_config')
@patch.object(NotionHelper, 'get_page_ids')
@patch.object(NotionHelper, 'get_page_content')
def test_successful_page_fetch(mock_get_page_content, mock_get_page_ids, mock_get_tool_config):
    mock_get_tool_config.return_value = 'TOKEN'
    mock_get_page_ids.return_value = ['id1', 'id2', 'id3']
    mock_get_page_content.return_value = 'content'
    result = notion_tool._execute('title')
    assert result == "Pages fetched successfully:\npage 1:\n\ncontent\npage 2:\n\ncontent\npage 3:\n\ncontent"


@patch.object(NotionfetchPageTool, 'get_tool_config')
@patch.object(NotionHelper, 'get_page_ids')
@patch.object(NotionHelper, 'get_page_content')
def test_get_page_content_error(mock_get_page_content, mock_get_page_ids, mock_get_tool_config):
    mock_get_tool_config.return_value = 'TOKEN'
    mock_get_page_ids.return_value = ['id1']
    mock_get_page_content.side_effect = Exception('Unable to fetch')

    result = notion_tool._execute('title')

    assert result == "Error: Unable to fetch page Unable to fetch"
