from unittest.mock import patch, Mock
import requests
import pytest

from notion_create_page import NotionCreatePageTool


@patch("requests.post")
@patch.object(NotionCreatePageTool, 'get_tool_config')
def test_notion_create_page_tool(mock_get_config, mock_post):
    # Data
    content_list = [{"type": "text", "content": "Test content", "language": "English"}]
    title = "Test Page"
    tags = ["tag1", "tag2"]

    # Here we are mocking the function call to get_tool_config to return test values.
    mock_get_config.side_effect = ["test_token", "test_database_id"]  # notion_token, notation_database_id in order

    # Response
    response_data = {
        "id": "test_id",
    }
    response = requests.Response()
    response.status_code = 200
    response.json = lambda: response_data    
    mock_post.return_value = response

    # Configure NotionCreatePageTool
    tool = NotionCreatePageTool()  # Now it is a no-arg constructor

    # Call 'execute' method
    result = tool._execute(content_list, title, tags)

    # Assertions
    assert result == "Page created successfully. Page ID: test_id"
    mock_post.assert_called_once_with(
        "https://api.notion.com/v1/pages",
        headers={"Authorization": "Bearer test_token", "Content-Type": "application/json", "Notion-Version": "2022-06-28"},
        data='{"parent": {"database_id": "test_database_id"}, "properties": {"title": {"title": [{"text": {"content": "Test Page"}}]}, "Tags": {"multi_select": [{"name": "tag1"}, {"name": "tag2"}]}}, "children": [{"object": "block", "type": "text", "text": {"rich_text": [{"text": {"content": "Test content"}}]}}]}'
    )