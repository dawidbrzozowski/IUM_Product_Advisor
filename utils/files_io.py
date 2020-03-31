import json
import os


def load_jsonl(path):
    with open(path, 'r') as json_file:
        lines = list(json_file)
        return [json.loads(line) for line in lines]

def write_json_file(filename, data):
    _, ext = os.path.splitext(filename)
    filename = filename if ext == ".json" else f'{filename}.json'
    with open(filename, 'w') as out_file:
        json.dump(data, out_file, ensure_ascii=False, indent=2)
