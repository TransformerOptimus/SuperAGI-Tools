import requests
import json

class NotionHelper:
    def __init__(self, notion_token):
        """
        Initializes the NotionHelper with the provided notion token.

        Args:
            Notion_token (str): Personal Notion token.
        """
        self.notion_token = notion_token
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def get_page_ids_payload(self,title,filter_type):
        return {
            "query": title,
            "sort": {
                "direction": "ascending",
                "timestamp": "last_edited_time"
            },
            "filter": {
                "value": filter_type,
                "property": "object"
            },
        }
    
    def get_page_ids(self,title,filter_type):
        response = requests.post("https://api.notion.com/v1/search", headers=self.headers, json=self.get_page_ids_payload(title,filter_type))
        response_data = response.json()
        ids=[]
        if "results" in response_data:
            for res in response_data["results"]:
                if title.lower() in res['properties']['Title']['title'][0]['plain_text'].lower():
                    ids.append(res['id'].replace('-',''))

        return ids

    def get_page_content(self,page_id):
        read_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        res = requests.request("GET", read_url, headers=self.headers)
        content_str=""
        for block in res.json()["results"]:
            if 'text' in block[block['type']]:
                if block[block['type']]['text'] and ('plain_text' in block[block['type']]['text'][0]):
                    content_str+=(f"{block[block['type']]['text'][0]['plain_text']}\n")
            elif 'rich_text' in block[block['type']]:
                if block[block['type']]['rich_text'] and ('plain_text' in block[block['type']]['rich_text'][0]):
                    content_str+=(f"{block[block['type']]['rich_text'][0]['plain_text']}\n")
        return content_str
    
    def create_page_children(self,content):
        children = []
        for index in range(0,len(content)):
            content_type=content[index]['type'].lower()
            children.append({
                "object": "block",
                "type":content_type ,
                content_type: {
                    **({"language": content[index]['language'].lower()} if content_type=="code" else {}),
                    "rich_text": [
                        {
                            "text": {
                                "content": content[index]['content'][:1900]
                            }
                        }
                    ]
                },
            })
        return children
    
    def create_page_properties(self,title,tags=None):
        return {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Tags": {"multi_select": [{"name": tag} for tag in tags]},
        }
    
    def create_page(self,content,title,database_id,tags=None):
        api_endpoint = f"https://api.notion.com/v1/pages"
        data = {
            "parent": {"database_id": database_id},
            "properties": self.create_page_properties(title,tags),
            "children":self.create_page_children(content),
        }
        return requests.post(api_endpoint, headers=self.headers, data=json.dumps(data))