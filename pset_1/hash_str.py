import os
from typing import Union
from hashlib import sha256

def get_csci_salt() -> bytes:
    """Returns the appropriate salt for CSCI E-29

    :return: bytes representation of the CSCI salt
    """

    # Hint: use os.environment and bytes.fromhex
    raw_salt = os.getenv("CSCI_SALT")
    salt = bytes.fromhex(raw_salt) if raw_salt!=None else None
    if not salt:
        raise ValueError("Salt returned cannot have the value '{}'\n"
                         "Are you using the pipenv shell?".format(salt))
    return salt


def hash_str(some_val: Union[str, bytes], salt: Union[str, bytes] = "") -> bytes:
    """Converts strings to hash digest

    See: https://en.wikipedia.org/wiki/Salt_(cryptography)

    :param some_val: thing to hash, can be str or bytes
    :param salt: Add randomness to the hashing, can be str or bytes
    :return: sha256 hash digest of some_val with salt, type bytes
    """
    salt = salt if type(salt)==bytes else salt.encode()
    some_val = some_val if type(some_val) == bytes else some_val.encode()
    return sha256(salt+some_val).digest()


def get_user_id(username: str) -> str:
    salt = get_csci_salt()
    return hash_str(username.lower(), salt=salt).hex()[:8]
