import requests
import json

class NotionHelper:
    def __init__(self, Notion_token):
        """
        Initializes the NotionHelper with the provided notion token.

        Args:
            Notion_token (str): Personal Notion token.
        """
        self.Notion_token = Notion_token
        self.headers = {
            "Authorization": f"Bearer {Notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def get_ids(self,title,filter_type):
        payload = {
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
        response = requests.post("https://api.notion.com/v1/search", headers=self.headers, json=payload)
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
        data = res.json()
        content_str=""
        for block in data["results"]:
            if 'text' in block[block['type']]:
                if block[block['type']]['text'] and ('plain_text' in block[block['type']]['text'][0]):
                    content_str+=(f"{block[block['type']]['text'][0]['plain_text']}\n")
            elif 'rich_text' in block[block['type']]:
                if block[block['type']]['rich_text'] and ('plain_text' in block[block['type']]['rich_text'][0]):
                    content_str+=(f"{block[block['type']]['rich_text'][0]['plain_text']}\n")
        return content_str
    
    def create_page(self,content,title,database_id,tags=None):
        api_endpoint = f"https://api.notion.com/v1/pages"
        children = []
        for i in range(0,len(content)):
            content_type=content[i]['type'].lower()
            children.append({
                "object": "block",
                "type":content_type ,
                content_type: {
                    **({"language": content[i]['language'].lower()} if content_type=="code" else {}),
                    "rich_text": [
                        {
                            "text": {
                                "content": content[i]['content'][:1900]
                            }
                        }
                    ]
                },
            })

        parent={
            "database_id": database_id
        }
        properties={
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
        data = {
            "parent": parent,
            "properties": properties,
            "children":children,
        }
        try:
            response = requests.post(api_endpoint, headers=self.headers, data=json.dumps(data))
            return response
        except Exception as err:
            return f"Failed to create page. {err}"