import json


def read_json_questions():
    with open("questions.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data['questions']
