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
