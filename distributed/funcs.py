from .models import Distribution
import json
from . import states
from .enums import Sides


def setup(config):
    """
    Loads a configuration file to setup the Main.

    Workers will NOT be configured, the configuration is done
    once the Worker is started for accepting Tasks.
    """

    with open(config) as f:
        conf = json.load(f)

    states.__ident__ = conf['ident']
    states.__side__ = Sides.MAIN


def distribution(workspace: str) -> Distribution:
    pass
