title: Python basics - Functions
date: 2021-07-31
modified: 2021-07-31
author: Alexey Tereshenkov
tags: python-basics, python 
slug: python-basics-functions
category: python-basics

[TOC]

This is one of the posts in a series of introductory Python articles. These posts explain programming principles in a simplified way and show very basic Python code that should help folks learning Python to get a better understanding of some concepts. In this post, I'll share some notes about writing and working with functions in Python that beginners may find useful. 

## Defining functions

Functions are used to include a piece of code that may be called multiple times from various parts of your program or code base. If you have multiple Python modules and each of them needs to execute the same piece of code, it makes sense to move this common code snippet into a separate module where you would make this code available as a function. 

There are multiple advantages of using functions (instead of having duplicate code present across multiple modules). Most importantly, if you define functions, when the code needs to be changed, it is changed only in one place and there is less code to maintain and read. It also becomes easier to [debug](https://en.wikipedia.org/wiki/Debugging) and to [refactor](https://en.wikipedia.org/wiki/Code_refactoring) the code.

Let's create a new function that will sum values within a collection.

```python
def calculate_sum(collection):
    """Return a sum of numbers within a collection."""
    result = 0
    for i in collection:
        result = result + i
    return result

calculate_sum([1, 2, 3, 4, 5])       
# 15
```

Python functions are defined using the `def` keyword; a function can also have some input arguments specified. The arguments can have arbitrary names, but it's helpful to name arguments based on what kind of values they will refer to.

The string in the triple quotes `Return a sum of numbers within a collection` is called a [docstring](https://www.python.org/dev/peps/pep-0257/) as this one provides documentation over what this function does. In order for this docstring to be accessible by Python internally and within your favorite IDE, it has to be on the first line after the `def` line.

Thereafter, the code that should be executed is added. The input arguments can be used within the function body as one usually wants to do some work with the values that have been supplied. However, it's not uncommon to use functions that do the same thing over and over again without really asking for any input data. Maybe you want to delete all files within a known location before proceeding any further and there is no need to specify the folder name when calling the function.

The last statement `return`, is always the last row of function code that will be executed. One usually wants to collect the results of the function execution, and this is exactly what the `return` statement does. In other words, in the code below, the variable `result` will refer to the value that the function returns, in this case, the sum of the input numbers. 

```python
result = calculate_sum([1, 5, 7])
``` 

Function doesn't have to return anything, such as with the case of cleaning up the folder, but it may be helpful to provide the caller with some feedback on the execution status (perhaps, a list of files that have been deleted).

## Return values for functions

Keep in mind that function can return not only scalar values such as numbers or strings, but essentially any kind of Python object including `None`, `False`/`True`, a class instance, a dictionary and so forth. What is even more interesting, is that even though a function can indeed return just a *single* object, this object can be a container of multiple objects. Let's build a function that will return a tuple of multiple pieces of statistics:


```python
from collections import Counter

def get_collection_stats(collection):
    """Return a tuple of average, mode, max, and min values"""   
    avg_val = int(sum(collection) / len(collection))
    max_val = max(collection)
    min_val = min(collection)
    mode_val = Counter(collection).most_common(1)[0][0]
    return (avg_val, max_val, min_val, mode_val)

(avg_value, max_value, min_value, mode_value) = get_collection_stats([3, 4, 5, 4, 6, 24, 32, 4, 12])
print("avg: ", avg_value)
print("max: ", max_value)
print("min: ", min_value)
print("mode: ", mode_value)

# ('avg:', 10)
# ('max:', 32)
# ('min:', 3)
# ('mode:', 4)
```

This function could have also returned a dictionary with keys being the statistical values of interest and one would access them with `result["max_value"]` and `result["min_value"]`.

## Making functions flexible

When creating new functions, it is often a good idea to make them environment agnostic, that is, independent of the current environment you are calling this function from. Let's build a function that will return some data stored in a file somewhere on your machine:

```python
def read_file():
    """Get contents of a file."""
    with open('/home/username/project/data/assets.csv') as f:
        lines = f.readlines()
    return lines
```

You may think that you will use this code just once and it will always run on your machine. However, as it turns out for many developers, the same code is later re-run on other machines and in other circumstances which makes it necessary to modify the code, such as update the machine or user name and adjust the file path. On one hand, it's impossible to foresee all things that could potentially may differ, and, of course, [YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it). On the other hand, it is a good idea to try to avoid hard-coding anything that could be either obtained from user as an input argument or even better be retrieved on-the-fly by using Python built-in or external modules.

There are dozens of other hardware, operating system, and Python related settings and parameters that can be obtained with the help of Python:


```python
import socket
# Getting machine name
print(socket.gethostname())

import sys
# Getting Windows version
print(sys.getwindowsversion())
# Getting Python version that is currently used and whether it is 32/64bit
print(sys.version)

import os
# Getting current logged in user name and home path; 
# os.environ gives access to the system environment variables
print(os.environ['HOME'])
print(os.environ['PATH'])
```

You could have retrieved the machine name from user, making it an input argument. However, since you can always obtain this at the execution time, there is really no need to do that unless the function needs to read the file on a different computer.

## Working with function arguments

Input arguments of a function may have a default value. This makes it possible for a user calling a function to define only those arguments that don't have any default value. For these arguments, users will need to supply  values explicitly:


```python
def clean_collection(input_collection, max_value=50, keep_strings=False):
    """Return a collection of values that are less than max_value
    and, optionally, without strings."""
    output_list = []
    for item in input_collection:
        if isinstance(item, str) and keep_strings:
            output_list.append(item)
        elif isinstance(item, int):
            if not max_value or item <= max_value:
                output_list.append(item)
    return output_list

clean_collection([1, 52, 'text2', 73, 10, 9, 'text1', 4, 7], 70, True)
# [1, 52, 'text2', 10, 9, 'text1', 4, 7]
```

The `keep_strings` boolean argument has a pre-defined default value which will force function to exclude the strings in the input list. If an item in the input list will be larger than `max_value` argument specified, it will be excluded.   

As your functions are small and don't have many arguments, specifying them in the same sequence as they were declared is relatively easy. However, some functions may take 10, 20, or more input arguments, such as [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv) function. This makes it difficult to understand what argument has been provided when calling the function. Therefore, it might be a good idea to supply the argument value together with its name when calling the function. This is particularly true when calling functions with a long list of arguments.


```python
clean_list(input_list=[1, 52, 73, 10, 9, 'text1', 4, 7],
           max_value=70,
           keep_strings=True)
```

Now, since the function has a default value for the `max_value` argument, you can omit this one when calling the function. However, it is not allowed to provide the non-keyword argument after the keyword argument:


```python
# correct syntax
clean_list(input_list=[1, 52, 73, 10, 9, 'text1', 4, 7],
           keep_strings=True)  
# incorrect syntax
clean_list(input_list=[1, 52, 73, 10, 9, 'text1', 4, 7],
           50)
```

Making the second function call results in a syntax error because Python interpreter is confused: for what argument have you supplied the `50` in the last call? To avoid this, always supply both value and the argument name - this is known as passing arguments by name. It is also worth mentioning that you can supply the arguments in an arbitrary order:


```python
clean_list(keep_strings=False,
           input_list=[1, 52, 73, 10, 9, 'text1', 4, 7],
           max_value=40)

clean_list(keep_strings=True, 
           input_list=[1, 52, 73, 10, 9, 'text1', 4, 7])
```

## Function naming

You can think of a function as a means of doing something. Thus, verbs are usually used when naming them. `get_current_date` is a good name for a function returning a current date; `current_date` is a poor name as it makes readers think that it is a variable referring to the current date. Even though there are no strict rules on how functions should be named, it might be a good idea to follow the common conventions for using certain verbs in certain contexts (`get`, `set`, `save`, `read`, `write`, `dump`, and so forth).

## Importing functions

When you saved your function in another module (Python file on disk), you can import this function by using the same `import` statement you use for importing standard library modules (which are also Python files stored in the Python installation directory). There are some best practices that are worth following. 

It is helpful to [organize the imports in a particular order](https://www.python.org/dev/peps/pep-0008/#imports) and import from modules only those functions and objects you are planning to use. So, instead of `import pandas` you could do `from pandas import DataFrame`. Your code will run quicker as there are fewer objects to import and it also gets easier to see what kind of objects you intend to use in your code. Another thing is that you won't need to type `pandas.DataFrame` as using the `DataFrame` will suffice (because we have imported the object from `pandas`, so it knows where it belongs). You could have also done `from pandas import DataFrame as df` using the alias for the imported module and then use `df` object in your code instead of typing the whole name. This is something you will often see with the `numpy` sample codes: `import numpy as np`.

A potentially dangerous `from numpy import *` will result in importing all of the objects found in the `numpy` package. Not only is this slow as lots of objects have to be loaded, but can also lead to the [name clashing](https://docs.python.org/2/tutorial/modules.html#more-on-modules) when you use the same name for your variables that have been used for the variables defined in the package you import. If you need to import multiple modules from the package, it is possible to do multiple imports in one line:


```python
from numpy import ndarray as nd, recarray as rec
```

Now you don't need to write `numpy.ndarray` as `nd` will suffice. However, make sure to stick to conventions; if `numpy` is often imported as `np` in the community of `numpy` developers, it's best to stick to this standard so that your code is more readable by others.

## Importing functions from other path

When you need to import a Python module stored somewhere else (not inside your project directory), there are multiple ways of doing this, but arguably the most straightforward one is to customize the `sys.path` property which contains all the folders where Python will look for the module names you supply. Imagine there is a Python module `/home/username/projectA/utils.py`. You are working in another directory, such as `/home/username/projectB`. If your Python module you are working with would be stored in the same directory as `utils.py`, you could just write `import utils`. However, as we are not in the same folder, we have to append `/home/username/projectA` to the path so Python could find the `utils` module.

There are often better ways to work with multiple directories that doesn't involve modifying the system path directly. Your projects could be installed in editable mode as packages into your development environment so that they'd become available on your system path. Many IDEs such as PyCharm and VSCode provide way to add project directories as sources directories (via settings) to let Python interpreter find the modules. Behind the scene, however, they are still extending the system path for Python, so it's very useful to understand how this works.

## Anonymous (lambda) functions

In Python, there are two ways of defining a function: using the `def` statement and `lambda` keyword. We have already created new functions using the `def` statement, so let's create a new function using `lambda` that will take an input list of integers and return `True` if an item in the list is even.


```python
is_even = lambda x: x % 2 == 0

for i in [1, 2, 3, 4]:
    print(is_even(i))
# False
# True
# False
# True
```

The code above could be rewritten without using the `lambda`:


```python
def is_even(x):
    return x % 2 == 0

for i in [1, 2, 3, 4]:
    print(is_even(i))
# False
# True
# False
# True
```

`lambda` has a slightly different syntax than a function and they have no `return` statement. But they could be handy for creating use once, throw away functions (that are unnamed). You might want use them when you need to do something with a data structure and you don't want to create a function for that:


```python
print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))
# [2, 4]

# without lambda
data = [1,2,3,4]
print([i for i in data if i % 2 == 0])
# [2, 4]
```

Lambda functions are also very helpful when providing the criteria for sorting a collection:

```python
data = [(10, "b"), (20, "c"), (30, "a")]

# sorting a collection of tuples based on the second elemen in each tuple
sorted(data, key=lambda item: item[1])
# [(30, 'a'), (10, 'b'), (20, 'c')]
```

You may see `lambda` used in other developers' code so it's helpful to understand how they work.

## Writing convenience functions

As your Python scripts get larger, you may find that you have some tiny snippets of Python code that are being used in multiple places. At this point of time, you may consider wrapping those snippets into functions which you could call. As those functions don't do anything except hiding verbose  calls to existing functions and methods (potentially with different arguments), they are sometimes called [convenience functions](https://en.wikipedia.org/wiki/Convenience_function).

For instance, you often need to find out the parent's directory name of a file. This can be done with the `Path("filepath").parent.name` from the `pathlib` module. However, as this line is fairly long, your code may get cluttered if it's used everywhere. You could wrap this single line into a tiny convenience function:


```python
from pathlib import Path

def parent(filepath):
    """Get name of the parent directory of a filepath."""
    return Path(filepath).parent.name
```

Or it could be that a 3rd party package you use to work with the file system breaks when attempting to delete a file that doesn't exist. To avoid cluttering your programs with repetitive checks for the file existence, you may like to wrap these calls into a tiny function to make your code less verbose:


```python
import filesystem # some 3rd party package
from pathlib import Path

def delete(filepath):
    """Delete a file ignoring non-existing files."""
    if Path(filepath).exists():
        filesystem.deep_delete(filepath)
        return True
    return False
```

Be cautious creating such convenience, or *helper*, functions though, as it may be not worth it. Having multiple helper functions used all around your project may make it difficult to read for other developers who are not familiar with them (unless your team have agreed on certain conventions). If you do use them, make sure to document their use properly. Also, be careful choosing a valid and meaningful name to avoid name collision with functions and classes from other Python modules.

Happy functioning!
