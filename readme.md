# Distributed

**This project is maybe not even started and consists of mostly only some of my views of what a distributed framework I want to write one. So nothing is guaranteed, and helps maybe welcomed. Well, at least I'm not thinking things that beyong my own capabilities.**

Distributed is a parallel computation framework for clusters to distribute serveral tasks over LAN, even WAN, while maintaining seamlessness and transparency of the main script, and without
much restrain of the distributed function.

In the best practice, should distributed functions be called without even a tiny extra bit of code other than setting up the things and unwrapping results, in implementations there maybe something not the same, like some constraint of paths or files, but will never be things that don't work.

```python
from time import sleep

def sleep_sum(a:int, b:int) -> int:
    sleep(1)
    return a+b

if __name__ == "__main__":
    print([sleep_sum(x, x+1) for x in range(10000)])
```

```python
# Comparing to its distributed alternative
from time import sleep
from distributed import distributed

@distributed(platform="*", threads=1)
def sleep_sum(a:int, b:int) -> int:
    sleep(1)
    return a+b

if __name__ == "__main__":
    '''
    Some necessary setup codes, like loading settings from
    some file, setting up and communicating with clusters.
    '''
    responses = [sleep_sum(x, x+1) for x in range(10000)]
    print([x.unwrap() for x in responses])
```

## 1. Concepts

The `Distributed` has its own set of models, to give a clear and comprehensive abstraction of the whole framework. Please read these if you want to know how I think the `Distributed` should work.

### 1.0 What we are executing

In a workflow, there are three things:

1. Actions that can not be executed parallely, you need to open a file before reading it.
2. Actions that can be executed parallely, like computing depth while annotating a sequence.
3. Actions that can be divided into actions, like align some sequences to a reference.

Of course, the distributed calculation framework does no job in case 1, but for case 2 and 3, obviously we can achieve more resource utilization by spread the calculation over machines. We define these as `parallelable tasks`, for the remained, they are `obstructive tasks`.

### 1.1 Main and Worker

Obviously, of any clustered calculation power, there should be something to give out works, and something else to consume them, and return the result of works. In the context of `Distributed`, let's call them the `Main` and the `Worker(s)`. They are named for avoiding some useless arguments, even though I'd prefer another ones.

A `Main` in is a machine that monitor, publish, and manages resource in the total network, for submitting `parallelable tasks` to other `Workers`, while solving `obstructive tasks` itself.

A `Worker` is a machine that has some, or all its system resources _scheduled out_ for the `Worker` client, to accept tasks from `Main`, execute them, and give a result out. `Workers` are **not** controlled by the `Main`, so in somehow you don't need to use dedicated machines to build up clusters, though dedicated ones will be much more efficient.

Though in a single workflow, there should be only one `Main` over a cluster of `Workers`, in multiple workflows there can be multiple `Main` distributing tasks to `Workers`. _They are decentralized._

So, workers may execute one, or even multiple tasks from different `Mains`, to avoid conflicts, both `Worker` and `Main` have their `local queue`: a queue stores multiple tasks that is executing, or pending to execute, tasks are executed in grouped isolated environments, which means, for any tasks, if they have a confirmed common workflow (not required to be a same file, but have same common `workspace` MD5), they are executed in a same isolated package, while they have different IOs or startup directories to avoid conflicts.

### 1.2 Workspace and Distribution

Where the functional codes lies in, is called `workspace`, to make sure the executed code in `Workers` have a same working environment as `Main` do, the workspace is compressed at startup, let's called the compressed one `distribution`, and distributed over network if `Workers` need it. Maybe an incremental check and sync mechanism will be implemented? Whatever.

Once recieved, `distribution` is unpacked into `workspace` in isolated folders, and if a task, or multiple tasks are coming, then `workspace` is loaded and things get imported like `Main` does, though in a `Worker` manner, in most of situation the environments should be identical, since they are actually loaded and imported in same setups, though in `Worker` the `distrbuted` functions may be hidden or just have no paralleled effect. I will try to think of if some sort of mechanism, which I currently called `redistribution` can be implemented later. We make sure that two sides both have a same `workspace`, so features that sounds quite impossible, like locally remote Exception handling, or transfering custom types with pickle, can be achieved without much effort.

### 1.3 Redistribution?

A `redistribution`, is some mechanism that I though, to make `Workers` able to also spread some of the calculation to other `Workers`. Right now there are two possible models for this, one is called `direct` and the other one is `relayed`.

### 1.4 Failures

Tasks are not guaranteed to be completed successfully, and sometimes they will just fail. Failed tasks will try to return the error occurred to the `Main`, and if `Task.unwrap()` is called then the error will be raised, or there will be other methods to check if a task completed safely and add something more to it.

## 2. Protocols

## 3. Concerns
