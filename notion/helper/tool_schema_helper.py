from pathlib import Path


class ToolSchemaHelper:
    @staticmethod
    def read_tools_schema_description(current_file: str, file_name: str) -> str:
        file_path = str(Path(current_file).resolve().parent) + "/description/" + file_name
        try:
            file = open(file_path, "r")
            file_content = file.read()
            file.close()
        except FileNotFoundError as e:
            raise e     
        return file_content