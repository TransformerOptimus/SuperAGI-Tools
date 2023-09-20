# Filename: assets/base_tool_client.py
from typing import List ,Optional, Type, Callable, Any, Union, Dict, Tuple 
from sqlalchemy.orm import Session
from superagi.tools.base_tool import BaseFileManager

class BaseToolClient:
    def __init__(self,session:Session):
        self.session = session
        self.file_manager = BaseFileManager(self,session)

    def use_file_manager_read_file(self, file_name):
        content = self.file_manager.read_file(file_name)
        return content
    
    def use_file_manager_write_file(self,file_name,content):
        result = self.file_manager.write_file(file_name,content)
        return result
     
    def query(self, *args, **kwargs): 
        # Add your query logic here
        pass   