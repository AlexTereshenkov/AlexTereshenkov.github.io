title: Python raising SyntaxError when having too many nested for loops
date: 2021-01-16
modified: 2021-01-16
author: Alexey Tereshenkov
tags: python
slug: python-too-many-nested-loops
category: python

[TOC]

## Overview

When writing programs in any programming language,
it is common to see some syntax or runtime errors.
For instance, in Python, it is easy to [mess up the indentation](https://www.flake8rules.com/rules/E101.html)
in a file after merging files from different codebases.
Likewise, one can make an [off-by-one error](https://en.wikipedia.org/wiki/Off-by-one_error) 
when accessing an array which will be found at the runtime only.

Some other types of errors, however, are very rare 
and it is likely that you will not see many of them in your lifetime as a
Python programmer.
For instance, if you never use recursion to process a large array,
you may never be hit by the [maximum recursion depth limitation](https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it)
that exists to guard against a stack overflow.

In this post, I document my findings around an issue I have faced
when attempting to run auto-generated Python code that contained
many nested `for` loops.

## Use case

I was working on a simple code generation library that given input numeric matrix 
would produce boilerplate Python program code that could be extended further.
I thought it would be useful to experiment how the tool would behave on a matrix
of many dimensions because that would involve creating quite a few nested loops.
I've been planning to start using `itertools.product` instead of relying on nested `for` loops,
but wanted to experiment before refactoring.

The generated Python code looked like this:

    :::python

    for i in range(1):
      print(0)
      for i in range(1):
        print(1)
        for i in range(1):
          print(2)
          # all the way to the 20th nested "for" loop 
          for i in range(1):
            print(18)
            for i in range(1):
              print(19)
              for i in range(1):
                print(20)

You can generate this Python code programmatically if you'd like to experiment:

    :::python

    loop = """{for_spaces}for i in range(1):
    {print_spaces}print({loop_number})\n"""

    code = ""
    for i in range(0, 21, 1):
        code += loop.format(
            for_spaces=" " * 2 * i,
            print_spaces=" " * 2 * i + "  ",
            loop_number=i,
        )
    print(code)

A very useful tool I've been using occasionally to verify that Python module
contains syntactically valid code is [`compileall`](https://docs.python.org/3/library/compileall.html)
which can be used both from a command line and in Python programs.
`compileall` tool will compile your source code into bytecode files (`.pyc`)
and if there are any syntax errors, the compilation will fail reporting the problem.

Bytecompiling the following Python code:

    :::python
    print "hello!"

produces

    :::bash
    $ python3 -m compileall code.py                     
    Compiling 'code.py'...
    ***   File "code.py", line 1
        print "hello!"
                    ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print("hello!")?

`compileall` has also been very useful when migrating legacy codebases from Python 2 to Python 3
when it was used for the first-level sanity check.

## Too many statically nested blocks

Bytecompiling the module with 20+ nested `for` loops:

    :::bash

    $ python3 -m compileall too_many_nested_for_loops.py 
    Compiling 'too_many_nested_for_loops.py'...
    ***   File "too_many_nested_for_loops.py", line None
    SyntaxError: too many statically nested blocks

It turns out that Python has a limit on how many nested blocks (so not just `for` loops)
one is allowed to have.
This seems to be a design decision that was made when the CPython interpreter was developed. 
CPython has a concept of a stack, namely `blockstack`, which is used to execute code blocks,
and it's maximum size is 20.

This is an internal implementation detail which I'd unlikely ever hit dealing with
human written Python code, but I find it to be very exciting to be able to see a low level detail
of CPython design. This [Stackoverflow question](https://stackoverflow.com/questions/44972719/why-does-python-have-a-limit-on-the-number-of-static-blocks-that-can-be-nested/44973363) 
provides a more thorough explanation of this limit.

Happy coding!
