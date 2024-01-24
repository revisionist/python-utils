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

#from .text import tidy_and_truncate_string

logger = logging.getLogger(__name__)


def parse_rfc_address(data):

    if data is None:
        return None
    elif isinstance(data, str):
        # If the data is a simple string, return it directly
        return data
    elif isinstance(data, dict):
        # If the data is a dictionary (object), parse it
        address = data.get('address', '')
        personal = data.get('personal', '')

        # Constructing the RFC address
        if personal and address:
            #return f'{personal}@{address}'
            return f'{personal}'
        elif personal:
            return personal
        elif address:
            return address
        else:
            return 'No valid address found'
    else:
        return None


def parse_rfc_address_list(address_list):

    parsed_addresses = [parse_rfc_address(address) for address in address_list if parse_rfc_address(address) is not None]
    
    return parsed_addresses if parsed_addresses else []


def format_rfc_addresses(address_list):
 
    parsed_addresses = parse_rfc_address_list(address_list)
    return ', '.join(parsed_addresses)
