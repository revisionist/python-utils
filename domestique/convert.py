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

logger = logging.getLogger(__name__)


def str_to_bool(value):
    if not value:
        return False
    if value.lower() in ('true', '1', 't', 'y', 'yes'):
        return True
    elif value.lower() in ('false', '0', 'f', 'n', 'no'):
        return False
    else:
        raise ValueError("Invalid boolean value")


def extract_object_by_property(objects, property_name, target_value):
    for obj in objects:
        if isinstance(obj, dict) and property_name in obj and obj[property_name] == target_value:
            return obj

    return None


def get_value_from_dict(dictionary, key):
    if dictionary and key in dictionary:
        return dictionary[key]
    return None


def get_dict_list_or_string(value):
    if value is None:
        return None
    elif isinstance(value, dict):
        return value
    elif isinstance(value, list):
        return value
    else:
        return str(value)


def get_dict_or_string(value):
    if value is None:
        return None
    elif isinstance(value, dict):
        return value
    else:
        return str(value)