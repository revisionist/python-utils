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
import uuid
import base64
import string
import random
import re

from . import _persistent


logger = logging.getLogger(__name__)


def base36_encode(number, alphabet=string.ascii_lowercase + string.digits):
    """Converts an integer to a base36 string."""

    base36 = ''

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def truncate_string(obj, max_length):

    if obj is None:
        return ""
    string_repr = str(obj)
    if len(string_repr) > max_length:
        return string_repr[:max_length] + '[...]'

    return string_repr


def truncate_string(obj, max_length):

    if obj is None:
        return ""
    string_repr = str(obj)
    if len(string_repr) > max_length:
        return string_repr[:max_length] + '[...]'

    return string_repr


def tidy_string(input_string):

    if not input_string:
        return ""
    string_repr = str(input_string)
    tidied_string = string_repr.replace('\n', '/')
    tidied_string = re.sub('<[^<]+?>', '', tidied_string)

    return tidied_string


def tidy_and_truncate_string(input_string, max_length):

    tidied_string = tidy_string(input_string)
    tidied_string = truncate_string(tidied_string, max_length)

    return tidied_string
