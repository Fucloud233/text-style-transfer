import json

def read_json(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def write_json(file_path: str, json_object):
    with open(file_path, 'w') as f:
        json.dump(json_object, file_path, indent=4)
        