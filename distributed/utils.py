import hashlib
from . import states
from .enums import Sides


def md5(fn):
    hash_md5 = hashlib.md5()
    with open(fn, 'rb') as f:
        for chunks in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunks)
    return hash_md5.hexdigest()
