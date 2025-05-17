import json


def json_formatter(data: list[dict]):
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    return json_str
