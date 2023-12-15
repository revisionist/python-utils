import logging
import uuid
import base64
import string
import random

from . import _persistent


logger = logging.getLogger(__name__)


def _base36_encode(number, alphabet=string.ascii_lowercase + string.digits):
    """Converts an integer to a base36 string."""

    base36 = ''

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def generate_id():

    return str(uuid.uuid4())


def generate_shorter_id(lowercase=False):

    if lowercase:
        uuid_int = int(new_uuid)
        base36_encoded = base36_encode(uuid_int)
        return base36_encoded
    else:
        new_uuid = uuid.uuid4()
        uuid_bytes = new_uuid.bytes
        b64_encoded = base64.b64encode(uuid_bytes)
        return b64_encoded.decode().replace('+', '').replace('/', '').replace('=', '')


def generate_simple_random_identifier(numchars=6, lowercase=True):

    if lowercase:
        return ''.join(random.choices(string.ascii_lowercase, k=numchars))
    else:
        return ''.join(random.choices(string.ascii_uppercase, k=numchars))

