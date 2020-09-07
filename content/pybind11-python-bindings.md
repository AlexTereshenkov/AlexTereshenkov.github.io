title: Building Python extension modules for C++ code with pybind11
date: 2020-08-11
modified: 2020-08-11
author: Alexey Tereshenkov
tags: python,pybind11,c++
slug: pybind11-python-bindings
category: python

[TOC]

### Introduction

If you ever needed to provide interface to the C/C++ code from your Python modules,
you may have used [Python extension modules](https://docs.python.org/3/extending/extending.html).
They are typically created when there is an existing C++ project and it is required to make it
accessible via Python bindings.
Alternatively, when performance becomes critical, a certain part of the Python project can be written
in C/C++ and made accessible to the rest of the Python codebase via some kind of interface.

Quite a few large C++ libraries and frameworks have associated Python bindings -- they can be used
for prototyping or simply to speed up the development as writing a Python program is supposed to take
less time than writing an equivalent C++ program.
Exposing your library interface with another popular language, such as Python, will also make your project
more accessible for programmers who are not very familiar with C++.

Refer to excellent [RealPython: Python Bindings: Calling C or C++ From Python](https://realpython.com/python-bindings-overview/)
article to learn more.

### Python bindings 

There are quite a few options on how you can make your C++ code accessible from Python.
However, I have personally worked only with `SWIG` and `pybind11` so far.
For now, let's focus on [`pybind11`](https://github.com/pybind/pybind11/blob/master/docs/basics.rst).
It's extremely easy to set up on Linux or Windows and you should be able to create a compiled Python
extension module (`.so` for Linux and `.pyd` for Windows) very quickly.

The [pybind11 documentation](https://pybind11.readthedocs.io/en/stable/basics.html) does provide excellent reference
information with a ton of examples.
However, those examples often demonstrate features in isolation 
and I thought it would be useful to share an example of a
more complete "library" where multiple examples are combined into something that looks like a MVP.

### Writing C++ code

Here is the C++ file, `Geometry.cpp`, I've written to demonstrate the `pybind11` features.
It showcases constructing custom `Point` class instances, finding the distance between them in 2D and 3D space, 
and overloading C++ comparison operators among a few other things.

{% include_code pybind11-python-bindings.cpp lang:cpp :hideall: %}

### Building a Python extension module

Once you have the `Geometry.cpp` file on disk and `pybind11` installed, you should be able to compile the C++ code
and link it to the Python headers:

    :::bash
    $ c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` Geometry.cpp -o Geometry`python3-config --extension-suffix`

If you are not very familiar with Bash, command in the backticks in the command above are evaluated by the shell before the main command. 

The `python3 -m pybind11 --includes` part is used to get the location of Python header files 
and the `python3-config --extension-suffix` part is used to get the suffix for the shared library name --
for CPython 3.6 on a 64bit Ubuntu, the `Geometry.cpython-36m-x86_64-linux-gnu.so` file will be created.

Now, once you have the shared library file, it can be imported and used pretty much as if it was a regular
Python module. 

### Using a Python extension module

Let's see our library in action by running the file `python3 use_geometry.py` containing the code below:

{% include_code pybind11-python-bindings.py lang:python :hideall: %}

The produced output:

    :::text
    __init__(*args, **kwargs)
    Overloaded function.
    1. __init__(self: Geometry.Point, x: float, y: float) -> None
    2. __init__(self: Geometry.Point, x: float, y: float, z: float) -> None

    distanceTo(self: Geometry.Point, point: Geometry.Point, in3D: bool = False) -> float
    Distance to another point

    Constructing a point with z set to nan
    Constructing a point with z set to nan
    Constructing a point with z set to nan
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Constructing a point with z set to a user given value
    Distance between Point (50, 60, 45) and Point (50, 60, 75) is 30.0
    Representation of the p1 is "Point (50, 60, 45)"
    Representation of the p2 is "Point (50, 60, 75)"

This is of course a very trivial example of `pybind11` usage, however there have been
successful attempts to use `pybind11` for binding existing large C++ libraries 
such as [CGAL](https://www.cgal.org/) and [Point Cloud Library](https://pcl.readthedocs.io/projects/tutorials/en/latest/#).
See an example of [wrapping some of the CGAL functionality with pybind11](https://github.com/rob-smallshire/mesher)
and [Python bindings for the Point Cloud Library](https://github.com/davidcaron/pclpy) to learn more.

Happy binding!