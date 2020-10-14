from typing import Dict
from . import states
from .enums import Sides


def __internal_setup_worker():
    states.__side__ = Sides.WORKER


def __internal_get_registry() -> Dict:
    return states.__distributed__
