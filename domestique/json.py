import logging
import json

logger = logging.getLogger(__name__)


def get_json_str_from_dict_or_str(input_item):

    if not input_item:
        raise ValueError("input_item must be a non-empty dictionary or a valid JSON string")

    if isinstance(input_item, dict):
        item_json = json.dumps(input_item)
    elif isinstance(input_item, str):
        try:
            item_json = json.loads(input_item)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided")
    else:
        raise TypeError("input_item must be a dictionary or a valid JSON string")

    return item_json


def get_dict_from_dict_or_json_str(input_item):

    if not input_item:
        raise ValueError("input_item must be a non-empty dictionary or a valid JSON string")

    if isinstance(input_item, dict):
        return input_item
    elif isinstance(input_item, str):
        try:
            return json.loads(input_item)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided")
    else:
        raise TypeError("input_item must be a dictionary or a valid JSON string")


def get_list_from_json_string(json_string):

    if json_string is None:
        return None
    try:
        parsed_data = json.loads(json_string)
        if isinstance(parsed_data, list):
            return parsed_data
    except json.JSONDecodeError:
        pass

    return None
