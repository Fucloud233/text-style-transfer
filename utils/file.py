import json
from pathlib import Path

def read_json(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json(file_path: str, json_object):
    with open(file_path, 'w') as f:
        json.dump(json_object, f, indent=4)

def modify_name(origin_file_path: str, file_name: str) -> str:
    file_path = Path(origin_file_path)
    return Path.joinpath(file_path.parent, file_name)
        