title: Python basics - Classes
date: 2021-08-01
modified: 2021-08-01
author: Alexey Tereshenkov
tags: python-basics, python 
slug: python-basics-classes
category: python-basics

[TOC]

This is one of the posts in a series of introductory Python articles. These posts explain programming principles in a simplified way and show very basic Python code that should help folks learning Python to get a better understanding of some concepts. In this post, I'll share some notes about writing and working with classes in Python that beginners may find useful. 

## Using an existing class

Python class is just a template of an object that we are using to model a certain entity or real world object, its properties and its behavior. For instance, a Python class can represent a file on a computer file system; such a class will have certain properties (or *attributes*) and behaviors (or *methods*). This way, a file class may have properties such as name, owner, permissions, and edit time. Its methods would be actions this object could do: for instance, we could ask file class to be renamed or moved and it also could tell us who its parent is.

`pathlib.Path` is a class that you may have already used probably without reflecting too much about its properties. We will start exploring the class concept with a simple `Path` class.


```python
from pathlib import Path

path = Path('/home/username/data/assets.csv')
```

We can create a new _instance_ of the class `Path` by assigning a variable to be equal to a class instance with certain default values supplied. A class constructor (the initialization method) has a number of default values it can take when you create an instance of this class. This far, we have created a `path` object which is a `Path` class instance that has many properties such as `name` and `suffix`. Because this instance is also a Python object, we can access its properties using the dot notation.

```python
print(panh.name, path.suffix)
```

Let's create an instance of another `Path` class. Note that it is possible to use object's methods on multiple class instances. For instance, it is possible to construct a `Path` object from two existing `Path` objects:


```python
from pathlib import Path

user_dir = Path('/home/user')
assets_file = Path('data/assets.csv')
path = Path(user_dir, assets_file)
print(path)
# /home/user/data/assets.csv
```

The `pathlib.Path` object also has _methods_. In other words, we can perform a certain operation on this object (you can think of methods as functions that are run on this specific object) and get some result back, just like we do when we run a function.

```python
# read file
path.read_text()
# remove file
path.unlink()

path = Path('/home/user/data/assets.csv')
path.relative_to('/home/user')
# PosixPath('data/assets.csv')
```

We have used the `relative_to` method of the `pathlib.Path` object and this method returned another object, `PosixPath` that has again own properties and methods. 

## Creating a new class

This far, we have only used existing classes that are present in `pathlib` module, but in fact you have already used many Python classes without ever thinking of that. For instance, variables you create in Python, such as lists and strings, are instances of the classes `list` and `str`, respectively. 

To create a class in Python, you use a special keyword `class`. Let's model an entity that is not present in `pathlib` to learn about classes and how they work. We will create a class that will represent an existing directory on the file system. Class definitions we write (just like we do with the function definitions using the `def` statements) must be executed before they can be used further in the code. 

```python
class Directory:
    """A file system directory."""
    
    def __init__(self, path):
        self.path = path
        
       
directory = Directory('/home/username/data')
print(directory)
# <__main__.Directory object at 0x00000284D5E6B7F0>

print(directory.path)
# /home/username/data
```

The only thing you need to specify is the special function `__init__` (constructor) that will run every time you will create an instance of this class. Because we will work with an existing directory, we have to supply a path to that directory. Passing the file system path as the input argument to the `__init__` function will let user specify the path to the directory when creating a class instance. The `directory` variable will represent the `Directory` class object.

A special word `self` that we used as the first argument is just a convention to refer to the object itself and you shouldn't worry about it for now. What is good to know though is that you can add your own properties to the class that will provide some useful information to the user. Let's add a property that will tell us the name of that directory:

```python
class Directory:
    """A file system directory."""
    
    def __init__(self, path):
        self.path = path
        self.name = Path(path).name
        
directory = Directory('/home/username/data')
print(directory.name)
# data
```

However, when we printed the `directory` variable out earlier, it didn't give us any useful information about the directory, only it's internal object representation which was rather cryptic. Thankfully, in Python you can override how the objects will be represented when they are printed out as well as when you access the object inside the interactive console (REPL).

```python
class Directory:
    """A file system directory."""
    
    def __init__(self, path):
        self.path = path
        self.name = Path(path).name
        
    def __repr__(self):
        return f'Directory("{self.path}")'
    
    def __str__(self):
        return str(self.path)
    
directory = Directory('/home/username/data')
print(directory)
# /home/username/data 

# inside REPL
directory
# Directory("/home/username/data")
```

As you will see, it is possible not only to get some basic information about the object, but actually call other functions and do a lot more. An object property can be a result of some calculation or data look-up. Let's add another useful property that will report names of the files inside the directory:


```python
class Directory:
    """A file system directory."""

    def __init__(self, path):
        self.path = path
        self.name = Path(path).name
        self.files = self.get_files()

    def get_files(self):
        return [item.name for item in Path(self.path).glob("*")
                if item.is_file()]

    def __repr__(self):
        return f'Directory("{self.path}")'

    def __str__(self):
        return str(self.path)
    
directory = Directory('/home/username/data')
print(directory.files)
```

## Class instance methods

As you see, it can be very convenient for a developer to have a class defined in another module and then just import the module, create a class instance and start using this object. You may wonder why couldn't we just write a function with the help of `Path`? We definitely could, but the true power of classes lies in how class instance objects can interact with each other. What can be implemented with the help of multiple functions can be often done with a more concise and elegant code of a class definition. 

To see that in action, let's define a new class - `CsvFile` that will represent a `.csv` file on disk.

```python
class CsvFile:
    """A csv file."""
    
    def __init__(self, path):
        self.path = path
```

This is no different from what we have already did with the `Directory` class. Let's add another property that will represent the data schema, that is, all the `.csv` file columns. The `columns` attribute will return the fields in the order they are stored in the `.csv` file (assuming the `.csv` file is comma-separated).

```python
class CsvFile:
    """A csv file."""

    def __init__(self, path):
        self.path = path
        self.columns = self.get_columns()
    
    def get_columns(self):
        with open(self.path) as fh:
            return next(fh).strip().split(',')


csv_file = CsvFile("/home/username/data/assets.csv")
print(csv_file.columns)
```

Now, what if we would like to check if two `.csv` files have the same schema? 

```python
assets2019 = CsvFile("/home/username/data/assets2019.csv")
assets2020 = CsvFile("/home/username/data/assets2020.csv")

print(assets2019.columns == assets2020.columns)
```

But what if we want to let users of our `CsvFile` class to compare the schema of two `.csv` files without taking into account the order of columns? Thinking of a database table, the concept of a column order doesn't make sense. Let's create a *method* that would compare the columns of two `.csv` files:


```python
class CsvFile:
    """A csv file."""

    def __init__(self, path):
        self.path = path
        self.columns = self.get_columns()
    
    def get_columns(self):
        with open(self.path) as fh:
            return next(fh).strip().split(',')

    def schema_match(self, other):
        """Compare the columns of two csv files."""
        return set(self.columns) == set(other.columns)
        

assets2019 = CsvFile("/home/username/data/assets2019.csv")
assets2020 = CsvFile("/home/username/data/assets2020.csv")

print(assets2019.schema_match(assets2020))
print(assets2019.columns == assets2020.columns)
```

The method `schema_match()` we wrote above takes as arguments `self` (the class instance itself) and `other` (another class instance object). It accesses the `columns` property for each of the objects and then compares the sets to make a decision whether the schema of the files matches. If two `.csv` files from the example above would have the same columns stored in different orders, the `assets2019.columns == assets2020.columns` would return `False`, but since their schema is identical, `assets2019.schema_match(assets2020)` would return `True`. We could also extend our method to provide more fine-grained control over the comparison protocol. Is comparison case sensitive? Are duplicate fields ignored? The method could even take an comparison configuration object where we could have defined all the comparison settings. 

## Advanced class behavior

When modeling a class behavior, it may be helpful to provide the logic of how the object should behave in various situations. For instance, it is possible to compare two `Path` objects:

```python
Path('/data/path') == Path('/data/path')
# True
Path('/data/path') == Path('/data/file')
# False
```

For the `.csv` files, at least in our business domain specification, we could say that two files are identical if they have the same name and the same schema. To do this, we have to tell Python to use a special method when deciding whether two objects are the same with the `__eq__` method:

```python
from pathlib import Path

class CsvFile:
    """A csv file."""

    def __init__(self, path):
        self.path = path
        self.name = Path(path).name
        self.columns = self.get_columns()
    
    def get_columns(self):
        with open(self.path) as fh:
            return next(fh).strip().split(',')

    def schema_match(self, other):
        """Compare the columns of two csv files."""
        return set(self.columns) == set(other.columns)

    def __eq__(self, other):
        return self.name == other.name and self.schema_match(other)


print(CsvFile("/home/username/data/assets2019.csv") == CsvFile("/home/username/data/assets2020.csv"))
```

It can also be useful to use an object in a `for` loop. For instance, we can let users of the `Directory` class iterate through the class instance and access every file stored within it. In order to do this, one has to use a special `__iter__` method.


```python
from pathlib import Path

class Directory:
    """A file system directory."""

    def __init__(self, path):
        self.path = path
        self.name = Path(path).name
        self.files = self.get_files()

    def get_files(self):
        return [item.name for item in Path(self.path).glob("*")
                if item.is_file()]
        
    def __iter__(self):        
        for f in self.files:
            yield f
            

directory = Directory("/home/username/data")

for filename in directory:
    print(filename)

# would return files one by one
scanner = iter(directory)
next(scanner)
```

All you need to define essentially is what kind of iteration you want to provide your users with. The `__iter__()`, called [generator function](http://stackoverflow.com/questions/47789/generator-expressions-vs-list-comprehension), works so that each time you use a `yield` statement, it will give you back the next item and then move to the next item in the list ready to be served. It may be helpful to learn a bit more about the generator expression as this technique may be necessary to use when dealing with large sequences or when the memory resources available are scarce. 

Keep in mind that the `scanner` generator from the example above is different from the `directory` (being iterable) because you can only iterate over the `scanner` once. This is because generators do not store all the iterable values in the computer memory, but generate them on-demand. You could construct a list of files while iterating the generator either in a standard `for` loop or with the help of list comprehension:


```python
scanner = iter(directory)
files = [item for item in scanner]
```

Keep in mind that when using the list comprehension, the entire list of items is created in memory. In contrast, while accessing the items in `.files` one by one, the generator accesses the items on-demand. This makes it possible to work with extremely large sequences without running out of memory.

Happy classing!
