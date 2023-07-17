from pathlib import Path


class ToolSchemaHelper:
    @staticmethod
    def read_tools_schema_description(current_file: str, file: str) -> str:
        file_path = str(Path(current_file).resolve().parent) + "/description/" + file
        try:
            f = open(file_path, "r")
            file_content = f.read()
            f.close()
        except FileNotFoundError as e:
            raise e     
        return file_content