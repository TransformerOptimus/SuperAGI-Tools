from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from improve_code import ImproveCodeTool
from write_code import CodingTool
from write_spec import WriteSpecTool
from write_test import WriteTestTool


class CodingToolkit(BaseToolkit, ABC):
    name: str = "CodingToolkit"
    description: str = "Coding Tool kit contains all tools related to coding tasks"

    def get_tools(self) -> List[BaseTool]:
        return [CodingTool(), WriteSpecTool(), WriteTestTool(), ImproveCodeTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return []
