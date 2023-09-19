# Filename: assets/base_tool_client.py
from typing import List ,Optional, Type, Callable, Any, Union, Dict, Tuple 
from base_tool import BaseTool, BaseToolkit, FileManager

class BaseToolClient:
    def __init__(self):
        self.tool = BaseTool()
        self.toolkit = BaseToolkit()
        self.file_manager = FileManager()

    def use_tool_execute_method(self, tool_input: Union[str, Dict], **kwargs: Any) -> Any:
        result = self.tool.execute(tool_input, **kwargs)
        return result

    def use_toolkit_get_tools(self):
        tools = self.toolkit.get_tools()
        return tools

    def use_file_manager_read_file(self, file_name):
        content = self.file_manager.read_file(file_name)
        return content
    
    def use_file_manager_write_file(self,file_name,content):
        result = self.file_manager.write_file(file_name,content)
        return result
        