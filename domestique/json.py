# Copyright 2023-2024 David Goddard.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import json
import json5

logger = logging.getLogger(__name__)


def get_json_str_from_dict_or_str(input_item):

    if not input_item:
        raise ValueError("input_item must be a non-empty dictionary or a valid JSON string")

    if isinstance(input_item, dict):
        item_json = json.dumps(input_item)
    elif isinstance(input_item, str):
        try:
            item_json = json5.loads(input_item)
        except json5.JSONDecodeError:
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
            return json5.loads(input_item)
        except json5.JSONDecodeError:
            raise ValueError("Invalid JSON string provided")
    else:
        raise TypeError("input_item must be a dictionary or a valid JSON string")


def get_list_from_json_string(json_string):

    if json_string is None:
        return None
    try:
        parsed_data = json5.loads(json_string)
        if isinstance(parsed_data, list):
            return parsed_data
    except json5.JSONDecodeError:
        pass

    return None
