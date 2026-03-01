import json
from typing import Any


def read_config(file_path: str) -> dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            return config_data
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: Configuration file '{file_path}' contains invalid JSON.")
        raise
    except (OSError, PermissionError) as e:
        print(f"Error: Could not read configuration file '{file_path}': {e}")
        raise
