
from typing import Callable
from .enums import Sides
from .models import Distributed, Sided, Proxy


def distributed(platform='*', threads=-1, memory=-1, strict=False):
    '''
    Transform a function to a distributed one.

    A distributed function should be the very atomic part of the pipeline,
    and can only be invoked from main. Any try of calling a distributed function
    on remotes, which usually happens when you have a `@distributed` that calls
    another one, will result in an error, since on workers distributed functions'
    namespaces are quickly destroyed once the analyze is complete, and only from
    main can invoke them.
    '''

    def distributed_wrapper(func):
        return Distributed(func, platform, threads, memory, strict)
    return distributed_wrapper


def sided(side: Sides):
    def sided_wrapper(func):
        return Sided(func, side)
    return sided_wrapper


def proxy(main: Callable, worker: Callable):
    def proxy_wrapper(_):
        return Proxy(main, worker)
    return proxy_wrapper


def singleton(clazz):
    '''
    Instantiate a class right after it is declared.

    The class should have no argument to initialize.
    '''
    return clazz()
