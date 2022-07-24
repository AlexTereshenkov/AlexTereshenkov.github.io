title: Python basics - Generators
date: 2022-07-23
modified: 2022-07-23
author: Alexey Tereshenkov
tags: python-basics, python 
slug: python-basics-generators
category: python-basics

[TOC]

This is one of the posts in a series of introductory Python articles. These posts explain programming principles in a simplified way and show very basic Python code that should help folks learning Python to get a better understanding of some concepts. In this post, I'll share some notes about writing and working with generators in Python that beginners may find useful. 

## Defining generators

At this point, you must be already with familiar with an iterator concept. Unfortunately, the terminology landscape is really confusing because there are iterables and iterators. Iterators are also iterable (because you can iterate them in a `for` loop), but iterator is not iterable (they return individual items with the `next()` call). And the terms `iterator` and `generator` are used as synonyms in the documentation most of the time.

Iterable (`items`): 

```python
items = [1,2,3]
for item in items:
    print(item)
```

Iterator (`producer`):

```python
producer = iter([1,2,3])  # type: list_iterator
next(producer)
# 1
next(producer)
# 2
next(producer)
# 3
next(producer)
# Traceback (most recent call last):
# ...
#    next(producer)
# StopIteration
```
    
The key difference between a "normal" function and a generator function is that a function returns a value whereas a generator function returns a generator. The returned generator can then produce (aka _yield_) values.

Function:

```python
def produce():
    return [1,2,3]


produce()
# [1, 2, 3] 
```

Generator function:

```python
def produce_generator():
    for item in [1,2,3]:
        yield item
        
produce_generator()
# <generator object produce_generator at 0x0000020284925660>

[i for i in produce_generator()]
# [1, 2, 3]

for i in produce_generator():
    print(i)

# 1
# 2
# 3
```

If you have used a list comprehension before, e.g. `[i*i for i in (1,2,3)]`, then understanding a generator expression would be easy since this is just a [lazy](https://en.wikipedia.org/wiki/Lazy_evaluation) version of a list comprehension -- the items are generated on demand.

```python
lazy_comp = (i for i in [1,2,3])
lazy_comp
# <generator object <genexpr> at 0x0000020284A4D740>

next(lazy_comp)
# 1
next(lazy_comp)
# 2
next(lazy_comp)
# 3
next(lazy_comp)
# Traceback (most recent call last):
# ...
#    next(lazy_comp)
# StopIteration
```

## Building generators

Generators (or generator functions) will become handy whenever you want to be able to produce values when it's required. Keep in mind that you can pass generators as function arguments since they "remember" their state and at what value they have stopped after the last request.

Here you can see how we pass a generator to a function after first getting a few values from it. It picks up where it was left!

```python
def produce_generator():
    for item in [1,2,3]:
        yield item
        

def resume(gen):
    return next(gen)


generator = produce_generator()
next(generator)
# 1
next(generator)
# 2
resume(generator)
# 3
```

When using the built-in `iter()` to create an iterator, it's helpful to remember that [`iter`](https://docs.python.org/3/library/functions.html#iter) takes a [sentinel](https://en.wikipedia.org/wiki/Sentinel_value) value which will tell the iterator to terminate when this value is produced.

In this example, we would like to obtain values from a generator until we get a certain value (sentinel value) and then we shall stop. Because the `iter` needs a callable for the first argument, we use `lambda` to delay the execution.

```python
def progress(val):    
    while True:
        val = val * 2
        yield val
        
producer = progress(2)
for i in iter(lambda: next(producer), 128):
    print(i)
    
# 4
# 8
# 16
# 32
# 64
```

Using a `lambda` in this context is fairly common. Here `lambda` is used in a generator expression to prevent evaluating too early:

```python
def download(url):
    print(f"Downloading from {url}")
    
    
callers = (
    lambda: download(url) for url in ["foo", "bar", "baz"]
)
print(callers)
# <generator object <genexpr> at 0x0000020284A4DDD0>

for caller in callers:
    caller()
        
# Downloading from foo
# Downloading from bar
# Downloading from baz
```

## Building an infinite generator

The [`itertools`](https://docs.python.org/3/library/itertools.html) module has a variety of useful generators. Attempting to re-implement some of them is a great exercise that will help you getting a deeper understanding of how generators work. Let's work on an infinite `cycle` generator that keeps producing the values from an iterable infinitely:

```python
def cycle(iterable):
    while True:
        for item in iterable:
            yield item
    
cycler = iter(cycle([1,2,3]))
next(cycler)
# 1
next(cycler)
# 2
next(cycler)
# 3
next(cycler)
# 1
next(cycler)
# 2
next(cycler)
# 3
# ...
```

This works, but this implementation is built on an assumption that user is going to create an iterator using the built-in `iter()`. Let's make this function return an iterator instead for a neater interface. For this, we can wrap the generator function inside another function:

```python
def cycle(iterable):
    def inf(iterable):
        while True:
            for item in iterable:
                yield item
    return iter(inf(iterable))


cycler = cycle([1,2,3])
next(cycler)
# 1
next(cycler)
# 2
next(cycler)
# 3
next(cycler)
# 1
next(cycler)
# 2
next(cycler)
# 3
# ...
```

## Delegating to a subgenerator: `yield from`

The `yield from` ([PEP 380](https://peps.python.org/pep-0380/)) provides another way to work with generators.

A standard approach for yielding values from a collection of containers is usually written as below:

```python
def flatten(*items):
    for item in items:
        for value in item:
            yield value
            
[i for i in flatten([10,20,30], [40,50,60])]
# [10, 20, 30, 40, 50, 60]
```

It can be rewritten as:

```python
def flatten(*items):
    for item in items:
        yield from item
            
[i for i in flatten([10,20,30], [40,50,60])]
# [10, 20, 30, 40, 50, 60]
```

In this example, this is just a bit nicer. The `yield from` can be used in coroutines which we are not going to talk about in this post. Note, however, that support for [generator-based coroutines](https://docs.python.org/3/library/asyncio-task.html#generator-based-coroutines) is deprecated and is removed in Python 3.11.

Another practical example of the delegation is when you need to `yield` from a generator within a generator itself.

### Using `yield from` to yield from a generator

Let's write a simple function that will produce paths of files within a given a directory, recursively. The `pathlib.Path.rglob()` would already do that for us, but we'd like to learn how `yield from` construct can be applied!

```python
def walk(path: Path):
  for subpath in path.glob("*"):
    if subpath.is_dir():
      yield walk(subpath)
    else:
      yield subpath

walker = walk(Path("/etc/apt"))
next(walker)
# PosixPath('/etc/apt/sources.list')
# ...
next(walker)
<generator object walk at 0x7f2ac323e430>
```

While iterating through items we find, if this is a file, then it's all good, but if we hit a directory, there's a problem. We cannot use `yield walk(subpath)` because `yield` would produce a generator (calling `walk()` returns a generator object). We therefore have to say that we would like to "step into" the generator and get an actual value this generator produces:

```python
def walk(path: Path):
  for subpath in path.glob("*"):
    if subpath.is_dir():
      yield from walk(subpath)
    else:
      yield subpath


walker = walk(Path("/etc/apt"))
next(walker)
# PosixPath('/etc/apt/sources.list')
next(walker)
# PosixPath('/etc/apt/sources.d/sources.list.distUpgrade')
```

I believe this example is very helpful to understand why you'd need the `yield from` construct.

### Using `yield`, `yield from`, and `return` in the same function

It's possible to use the `return` statement within a generator function. When `return` is hit, the function actually returns a value and stops:

```python
def get(iterable):
    for item in iterable:
        if item > 2:
            return
        yield item


getter = get([1,2,3,4])
for item in getter:
    print(item)
    
1
2
```

Now, let's write a function that will return a flattened version of an iterable up to a certain value.

```python
from typing import List


def search(haystack: List[int], needle: int):
    """Find a needle in a haystack."""
    for item in haystack:
        if isinstance(item, list):
            print(f"Looking at: {item}")
            yield from search(item, needle)
        else:
            if needle == item:
                yield item
                print(f"found {item}")
                return
            else:
                print(f"Looking at: {item}")
                yield item


assert list(
    search(haystack=[1,[2,[3,4,5,6]]], needle=4)
    ) == [1,2,3,4]

# Looking at: 1
# Looking at: [2, [3, 4, 5, 6]]
# Looking at: 2
# Looking at: [3, 4, 5, 6]
# Looking at: 3
# found 4
```

When iterating over the `haystack`, if we get an iterable (a `list` in this particular case), then we want to `yield from` the iterable, recursively. If the value we found is our `needle`, then we have to `return` and terminate immediately. Even though our `return` statement was called deep inside a recursive `yield from` call, the program stopped there.

---

If you'd like to follow up, you may want to learn about [the methods of a generator iterator](https://docs.python.org/3/reference/expressions.html#generator-iterator-methods) which can be used to control the execution of a generator function and later on proceed to the [Asynchronous generator functions](https://docs.python.org/3/reference/expressions.html#asynchronous-generator-functions).

Happy generating!
