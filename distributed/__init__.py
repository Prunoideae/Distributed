from functools import partial, wraps

__doc__ = '''
Distributed
===========

A seamless, transparent framework for parallel calculation through 
network.
'''


def distributed(func=None, *, platform='*', threads=-1, memory=-1, strict=False):
    '''
    Transform a function to a distributed one.

    A distributed function should be the very atomic part of the pipeline,
    and can only be invoked from main. Any try of calling a distributed function
    on remotes, which usually happens when you have a `@distributed` that calls
    another one, will result in an error, since on workers distributed functions'
    namespaces are quickly destroyed once the analyze is complete, and only from
    main can invoke them.
    '''
    pass
