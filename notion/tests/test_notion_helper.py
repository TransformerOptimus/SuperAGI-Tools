import pytest
import requests
import json
from unittest.mock import patch
from ..helper.notion_helper import NotionHelper

@patch('requests.post')
def test_get_page_ids(mock_post):
    # Mock the response from requests.post
    mock_response = mock_post.return_value
    mock_response.json.return_value = {
        "results": [{
            "properties": {
                "Title": {
                    "title": [{
                        "plain_text": "Testing Title"
                    }]
                }
            },
            "id": "12345"
        }]
    }

    notion_helper = NotionHelper("token")
    ids = notion_helper.get_page_ids("Testing Title", "page")

    assert ids == ["12345"]

@patch('requests.request')
def test_get_page_content(mock_request):
    mock_response = mock_request.return_value
    mock_response.json.return_value = {
        "results": [{
            "type": "text",
            "text": [{"plain_text": "Mock Content"}]
        }]
    }
    
def test_create_page_children():
    notion_helper = NotionHelper("token")

    content = [{'type': 'text', 'content': 'This is some test content'}]

    expected_output = [{
        "object": "block",
        "type": 'text',
        'text': {
            "rich_text": [{"text": {"content": 'This is some test content'}}]
        }
    }]

    assert notion_helper.create_page_children(content) == expected_output


@patch('requests.post')
def test_create_page(mock_post):
    mock_response = mock_post.return_value
    mock_response.json.return_value = {"object": "page"}

    # Initialize NotionHelper and get page ids
    notion_helper = NotionHelper("token")
    content = [{"type": "text", "content": "Mock Content"}]
    resp = notion_helper.create_page(content, "Test Page", "12345", ["TestTag1", "TestTag2"])
    
    assert resp.json() == {"object": "page"}

@pytest.mark.parametrize('text,expected', [('some test text', 7), ('', 4), ('one word', 6)])
def test_count_text_tokens(text, expected):
    notion_helper = NotionHelper("token")
    assert notion_helper.count_text_tokens(text) == expected