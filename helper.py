import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def read_json_file(filepath):
    """Read a JSON file and return its contents as a Python object."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(filepath, data):
    """Write a Python object to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
