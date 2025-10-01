# Copyright 2023-2025 David Goddard.
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

from __future__ import annotations

import logging
import uuid
import base64
import string
import secrets


_B62 = string.digits + string.ascii_uppercase + string.ascii_lowercase
_B36_LOWER = string.digits + string.ascii_lowercase


def _base36_encode(
    number: int,
    alphabet: str = string.ascii_lowercase + string.digits,
) -> str:

    if number < 0:
        raise ValueError("number must be non-negative")

    base36 = ""
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def _encode_base_n(number: int, alphabet: str) -> str:

    if number < 0:
        raise ValueError("Number must be non-negative")
    base = len(alphabet)
    if base < 2:
        raise ValueError("Alphabet must contain at least 2 characters")
    if number == 0:
        return alphabet[0]
    out = []
    while number:
        number, rem = divmod(number, base)
        out.append(alphabet[rem])
    out.reverse()
    return "".join(out)


def _uuid_to_fixed_base(u: uuid.UUID, alphabet: str, width: int) -> str:

    s = _encode_base_n(u.int, alphabet)
    if len(s) > width:
        raise ValueError("Encoded value exceeded expected width")

    return s.rjust(width, alphabet[0])


def generate_id() -> str:
    """Return a UUID4 string as ID"""

    return str(uuid.uuid4())


def generate_shorter_id(lowercase: bool = False) -> str:
    """
    Short, fixed-length, alphanumeric-only ID from UUID4.

    - lowercase=False: base-62, 22 chars, [0-9A-Za-z]
    - lowercase=True : base-36 (lowercase), truncated to 22 chars, [0-9a-z]
    """
    u = uuid.uuid4()
    if lowercase:
        # Base-36 is ~25 chars for 128 bits. Pad to 25, then take the last 22.
        b36_25 = _uuid_to_fixed_base(u, _B36_LOWER, width=25)
        return b36_25[-22:]
    else:
        # Full base-62 fits in 22 chars without truncation.
        return _uuid_to_fixed_base(u, _B62, width=22)


def generate_simple_random_identifier(
    numchars: int = 6,
    lowercase: bool = True,
    include_numbers: bool = False,
    prefix: str = None,
    suffix: str = None,
) -> str:
    """
    Generate a random identifier composed of letters (and optionally digits),
    with optional prefix/suffix. Uses `secrets` for randomness.

    Args:
        numchars: Number of random characters (must be >= 1).
        lowercase: If True, use a–z; else use A–Z.
        include_numbers: If True, include 0–9 in the alphabet.
        prefix: Optional string to prepend.
        suffix: Optional string to append.
    """

    if numchars < 1:
        raise ValueError("numchars must be >= 1")

    letters = string.ascii_lowercase if lowercase else string.ascii_uppercase
    alphabet = letters + (string.digits if include_numbers else "")

    id = "".join(secrets.choice(alphabet) for _ in range(numchars))
    
    if prefix:
        id = f"{prefix}{id}"
    if suffix:
        id = f"{id}{suffix}"
        
    return id


def generate_simple_hex_identifier(
    numchars: int = 6,
    lowercase: bool = True,
    prefix: str = "",
    suffix: str = "",
) -> str:
    """
    Generate a random hex string (0–9, a–f/A–F) with optional prefix/suffix.

    Args:
        numchars: Number of hex characters (must be >= 1).
        lowercase: If True, use lowercase hex; else uppercase.
        prefix: Optional string to prepend.
        suffix: Optional string to append.
    """

    if numchars < 1:
        raise ValueError("numchars must be >= 1")

    hexdigits = "0123456789abcdef" if lowercase else "0123456789ABCDEF"
    id = "".join(secrets.choice(hexdigits) for _ in range(numchars))

    if prefix:
        id = f"{prefix}{id}"
    if suffix:
        id = f"{id}{suffix}"

    return id
