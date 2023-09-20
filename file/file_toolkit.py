from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from append_file import AppendFileTool
from delete_file import DeleteFileTool
from list_files import ListFileTool
from read_file import ReadFileTool
from write_file import WriteFileTool
from superagi.types.key_type import ToolConfigKeyType
from superagi.models.tool_config import ToolConfig


class FileToolkit(BaseToolkit, ABC):
    name: str = "File Toolkit"
    description: str = "File Tool kit contains all tools related to file operations"

    def get_tools(self) -> List[BaseTool]:
        return [AppendFileTool(), DeleteFileTool(), ListFileTool(), ReadFileTool(), WriteFileTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
