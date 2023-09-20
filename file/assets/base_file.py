# Filename: assets/base_tool_client.py
from typing import List ,Optional, Type, Callable, Any, Union, Dict, Tuple 
from sqlalchemy.orm import Session
from superagi.tools.base_tool import BaseFileManager

class BaseToolClient:
    def __init__(self,Session:Session):
        self.file_manager = BaseFileManager(self,Session)

    def use_file_manager_read_file(self, file_name):
        content = self.file_manager.read_file(file_name)
        return content
    
    def use_file_manager_write_file(self,file_name,content):
        result = self.file_manager.write_file(file_name,content)
        return result
        