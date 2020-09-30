'''
A class for storing global data, like machine side, collected info
or queue.

Not meant to be used externally in any means, just for internal states.
'''
from os import cpu_count
import sys
import math
import psutil

__side__ = None

__queue__ = []

__ident__ = None

__distributed__ = []


class __sys__:
    def __init__(self) -> None:
        self.platform = sys.platform
        self.bit = int(math.log2(sys.maxsize + 1) + 1)
        self.threads = cpu_count()

    @property
    def memory(self) -> int:
        return psutil.virtual_memory().available

    def disk(self) -> int:
        pass


__sys__ = __sys__()
