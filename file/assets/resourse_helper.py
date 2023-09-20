from typing import Type 
from base_tool import BaseResourceHelper

class ResourceClient:
    def __init__(self):
        self.resource_helper = BaseResourceHelper()

    # Direct implementations of BaseResourceHelper methods
    def use_get_formatted_agent_level_path(self, agent, path):
        return self.resource_helper.get_formatted_agent_level_path(agent, path)
    
    def use_get_formatted_agent_execution_level_path(self, agent_execution, path):
        return self.resource_helper.get_formatted_agent_execution_level_path(agent_execution, path)
    
    def use_get_resource_path(self, file_name):
        return self.resource_helper.get_resource_path(file_name)
    
    def use_get_root_output_dir(self):
        return self.resource_helper.get_root_output_dir()
        
    def use_get_root_input_dir(self):
        return self.resource_helper.get_root_input_dir()
    
    def use_get_agent_write_resource_path(self, file_name, agent, agent_execution):
        return self.resource_helper.get_agent_write_resource_path(file_name, agent, agent_execution)
    
    def use_get_agent_read_resource_path(self, file_name, agent, agent_execution):
        return self.resource_helper.get_agent_read_resource_path(file_name, agent, agent_execution)