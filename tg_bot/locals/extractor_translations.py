import json

def get_tranclations(tranclations_file: str):
    with open(tranclations_file, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data