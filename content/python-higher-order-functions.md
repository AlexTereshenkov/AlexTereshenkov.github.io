title: Introduction to higher order functions with Python
date: 2021-03-11
modified: 2021-03-11
author: Alexey Tereshenkov
tags: python,functional-programming
slug: python-higher-order-functions-intro
category: python

[TOC]

## Overview

Python is not considered to be a functional language, however it does support the functional
paradigm.
The Python documentation provides a gentle introduction to 
[functional programming](https://docs.python.org/3/howto/functional.html) with excellent narrative.
As I continue to learn [ML](https://en.wikipedia.org/wiki/ML_(programming_language)), 
I wanted to share a few interesting concepts around higher-order functions with a few examples
written in Python.

## What is a higher-order function?

In Python, functions are [first-class](https://en.wikipedia.org/wiki/First-class_function) 
which means that a developer can pass functions as arguments to other functions,
a function can return a function, and a function can be assigned to a variable or stored in 
some data structure.

A higher-order function, in contrast, is a function that either (or both)

* takes one or more functions as arguments 
* returns a function as its result

The `map` built-in function is an excellent example of a higher order function as you pass a function
as an argument:

    :::python
    >>> list(map(lambda x: x**x, [1, 2, 3]))
    [1, 4, 27]

A decorator is also a higher-order function because it takes a function as an argument
and returns a function:

    :::python
    def twice(func):
        def caller(**args):
            func(**args)
            func(**args)
        return caller
    
    
    @twice
    def work():
        print("Doing work")

The `work` function will be executed twice because it has been decorated with the `twice` decorator:    

    :::python
    >>> work()
    Doing work
    Doing work

## Examples of higher-order functions

### Call a function multiple times re-using the result

A function that given `x`, will call `f(x)` the `n` times.
The result of each call will become input for the subsequent call.
For instance, `do_ntimes(lambda x: x+x, 3, 1)` is `8` because
`1 + 1 = 2` and now it's `2 + 2 = 4` and then finally `4 + 4 = 8`.
This happens using a [recursive call](https://alextereshenkov.github.io/python-recursion-intro.html).

    :::python
    def do_ntimes(f, n, x):
        """Higher-order function that will do an operation f
        on x the n times.
        >>> do_ntimes(lambda x: x+x, 3, 1)
        8
        >>> do_ntimes(lambda x: x+x, 10, 1)
        1024
        """
        if n == 0:
            return x
        else:
            return f(do_ntimes(f, n - 1, x))

### Function composition with two functions

[Function composition](https://en.wikipedia.org/wiki/Function_composition) 
is the process of combining two function calls into a single one.

    :::python
    def compose_two(f, g):
        """Function composition of two functions.
        >>> compose_two(f=lambda x: x + 10, g=lambda x: x - 5)(10)
        15
        >>> compose_two(f=lambda x: x - 25, g=lambda x: x * 10)(10)
        75
        """
        fg = lambda x: f(g(x))
        return fg

It is possible to pass the lambda functions directly or by assigning them
to variables first:

    :::python
    >>> compose_two(f=lambda x: x + 10, g=lambda x: x - 5)(10)
    15
    >>> add10 = lambda x: x + 10
    >>> minus5 = lambda x: x - 5
    >>> compose_two(f=add10, g=minus5)(10)
    15

### Reducing to calculate the factorial

In addition to a recursion based solution (or a plain loop), it's also possible to calculate
factorial of a number using the `functools.reduce`:

    :::python
    from functools import reduce
    from operator import mul


    def factorial_reduce(n):
        """Calculate factorial.
        >>> factorial_reduce(5)
        120
        """
        return reduce(mul, range(1, n + 1), 1)

### Reducing a chain of function calls

The function composition example can be rewritten in a standalone call.
This is done using the built-in `functools.reduce()` function call.
The result of the first function execution becomes the input argument
for the next function.
In the example below, the operation is `( ( (0 + 10) * 3 ) / 2 )`.

    :::python
    >>> reduce(lambda res, f: f(res), 
    [lambda n: n + 10, lambda n: n * 3, lambda n: n / 2], 0)
    15.0

### Function composition with arbitrary number of functions

Building up on the example above, the `compose` function can take
[arbitrary arguments](https://docs.python.org/dev/tutorial/controlflow.html#arbitrary-argument-lists) 
wrapped up in a tuple.

    :::python
    def compose(*functions):
        """Function composition of arbitrary number of functions.
        >>> compose(*(lambda x: x + 2, lambda x: x + 5, lambda x: x - 6))(10)
        11
        >>> compose(*(lambda x: x + 2,))(10)
        12
        """
        fg = lambda value: reduce(lambda res, f: f(res), functions, value)
        return fg

### Currying to check if elements are sorted

When one is [currying](https://en.wikipedia.org/wiki/Currying) a function, 
one is converting a function that takes multiple arguments into a sequence of functions that each take a single argument.

    :::python
    def are_3elems_sorted():
        """Use currying to check if three elements are sorted.
        >>> ((are_3elems_sorted()(1))(2))(3)
        True
        >>> ((are_3elems_sorted()(1))(4))(3)
        False
        """
        return lambda x: lambda y: lambda z: z > y > x


Happy functioning!
