import pickle
from sys import modules
from .utils import md5
from io import UnsupportedOperation
from . import states
from .enums import Sides
import sys
from typing import Any, Callable
from os import path
import tarfile


class RemoteExectionError(Exception):
    def __init__(self, exc, source) -> None:
        self.exc = exc
        self.source = source

    def __str__(self) -> str:
        return f"Remote {self.source} - " + self.exc.__str__()


class Result():

    def __init__(self, result, source) -> None:
        self.result = result
        self.source = source
        self.__exc__ = isinstance(result, Exception)
        if self.__exc__:
            _, _, tb = sys.exc_info()
            self.result = RemoteExectionError(result, tb).with_traceback(tb)

    def unwrap(self) -> Any:
        if self.__exc__:
            raise self.result.with_traceback(self.result.tb)
        return self.result

    def is_err(self):
        return self.__exc__

    def ok(self) -> Any:
        return self.result if not self.__exc__ else None


class Task():
    def __init__(self) -> None:
        pass

    def wait(self):
        pass


class Distributed():

    def __init__(self, func: Callable, platform, threads, memory, strict) -> None:
        self.ident = f'{func.__module__}/{func.__name__}'
        states.__distributed__[self.ident] = func

        self.platform = platform
        self.threads = threads
        self.memory = memory
        self.strict = strict

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if states.__side__ != Sides.MAIN:
            raise UnsupportedOperation("Cannot submit a Worker function on Worker side.")

        uid = f'{states.__ident__}@{self.ident}'
        arg = pickle.dumps((args, kwds))

        # TODO: handle the request and return a task
        states.__queue__.append(Task())


class Sided():

    def __init__(self, func: Callable, side: Sides) -> None:
        self.func = func
        self.side = side

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if states.__side__ != self.side:
            return None
        return self.func(*args, **kwds)


class Proxy():

    def __init__(self, main: Callable, worker: Callable) -> None:
        self.main = main
        self.worker = worker

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if states.__side__ == Sides.MAIN:
            return self.main(*args, **kwds)
        else:
            return self.worker(*args, **kwds)


class Distribution():

    def __init__(self, workspace: str, entry: str) -> None:

        if not path.isdir(workspace):
            raise UnsupportedOperation("Can only compress directory as distribution!")

        workspace = path.abspath(workspace)
        entry = path.abspath(entry)

        if workspace not in entry:
            raise UnsupportedOperation("Distribution entry not found in workspace!")

        self.path = path.join(workspace, f"{states.__ident__}.tar.gz")
        with tarfile.open(workspace, 'w:gz') as tar:
            tar.add(workspace, arcname=path.basename(workspace))

        self.md5 = md5(self.path)
