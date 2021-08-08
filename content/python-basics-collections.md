title: Python basics - Collections
date: 2021-08-08
modified: 2021-08-08
author: Alexey Tereshenkov
tags: python-basics, python 
slug: python-basics-collections
category: python-basics

[TOC]

This is one of the posts in a series of introductory Python articles. These posts explain programming principles in a simplified way and show very basic Python code that should help folks learning Python to get a better understanding of some concepts. In this post, I'll share some notes about working with useful containers from the `collections` module and various data structures that beginners may find useful. 

## `collections.defaultdict`

When iterating over some text files or any other kind of data structures, you may want to construct a dictionary with the key referring to a single object (e.g., a string) and the values referring to a list of objects (e.g., strings). However, when you create a new dictionary, there are no keys present, so you first have to add an empty list as the value for each of the keys and then start appending strings to the respective lists. Let's see how it works on a simpler example first. We cannot append a city name to the dictionary's key value as there is no list created yet, so we have to initialize the value making it an empty list for all new keys we find.

```python
d = {}
data = [('Zone', 'West'), ('Zone', 'East'), 
        ('Cluster', 'US'), ('Cluster', 'EU')]

for key, value in data:
    if key not in d:
        d[key] = []
    d[key].append(value)
print(d)
# {'Zone': ['West', 'East'], 'Cluster': ['US', 'EU']}
```

Using the `collections.defaultdict`, it is possible to create a dictionary structure where every key will already have a pre-assigned value of a certain type, such as `list` or `int`. This results in much cleaner code.


```python
from collections import defaultdict

dd = defaultdict(list)
data = [('Zone', 'West'), ('Zone', 'East'), 
        ('Cluster', 'US'), ('Cluster', 'EU')]

for key, value in data:
    dd[key].append(value)
print(dd)

# defaultdict(<class 'list'>, {'Zone': ['West', 'East'], 'Cluster': ['US', 'EU']})
```

This could also be done using the dictionary's `setdefault()` method. This means that a default value, which is an empty list in this case, will always be computed if the key is not present in the dictionary yet.

```python
sd = {}
data = [('Zone', 'West'), ('Zone', 'East'), 
        ('Cluster', 'US'), ('Cluster', 'EU')]

for key, value in data:
    sd.setdefault(key, []).append(value)
print(sd)
# {'Zone': ['West', 'East'], 'Cluster': ['US', 'EU']}
```

Another neat feature of a dictionary is that it is possible to get a default value if a key is not present. This is done by using the `get()` method for which you can supply a default value. In the code snippet below, as there is no `Port` key in the dictionary, instead of getting `None`, we would like to get some default value instead.

```python
d = {'LogLevel': 'Verbose', 'Database': 'Production'}
print d.get('LogLevel')
print d.get('Database')
print d.get('Machine')
print d.get('Port', 1433)
# Verbose
# Production
# None
# 1433
```

##  `collections.namedtuple`

Another useful class from the `collections` module is `namedtuple`. This one becomes very handy when working with tuples of many items particularly when you need to access the individual items within a tuple. Usually records returned from a database table are represented as lists of tuples. Named tuples let you access fields of the returned records by name rather than by index. When working with a tuple of potentially a hundred fields, it is easy to make mistakes in indexing and access a wrong field. Compare these two snippets and see how more readable the second one is. With the named tuple, you can refer to a field by its name instead of using the `[index]` syntax:


```python
# using tuple indexing for accessing database table fields 
envs = [
    ("Development", "west-us", 27134),
    ("Staging", "east-us", 48628),
    ("Production", "west-eu", 78951),
]
 
for env in envs:
    print("Environment {name} in {cluster} had {requests} requests".format(name=env[0], cluster=env[1], requests=env[2]))
# Environment Development in west-us had 27134 requests
# Environment Staging in east-us had 48628 requests
# Environment Production in west-eu had 78951 requests
```

The same information represented with the help of named tuples:

```python
# using named tuples for accessing database table fields
from collections import namedtuple

envs = [
    ("Development", "west-us", 27134),
    ("Staging", "east-us", 48628),
    ("Production", "west-eu", 78951),
]

Environment = namedtuple('Environment', ['Name', 'Cluster', 'Requests'])
environments = [Environment(*env) for env in envs]

print(environments[0]) # named tuple object

for env in environments:
    print("Environment {name} in {cluster} had {requests} requests".format(name=env.Name, cluster=env.Cluster, requests=env.Requests))

# Environment(Name='Development', Cluster='west-us', Requests=27134)

# Environment Development in west-us had 27134 requests
# Environment Staging in east-us had 48628 requests
# Environment Production in west-eu had 78951 requests
```

## List and dictionary comprehensions

One may need to construct a dictionary from some other data structure such as a JSON file or a collection of records such as a list of tuples. Regardless of the data structure that is being used, a _dictionary comprehension_ provides an intuitive and easy to read interface for creating a dictionary in a very similar way to how lists are constructed with the help of list comprehensions.

```python
envs = [
    ("Development", "west-us", 27134),
    ("Staging", "east-us", 48628),
    ("Production", "west-eu", 78951),
]

d = {env[0]: env[1] for env in envs}
print(d)
# {'Development': 'west-us', 'Staging': 'east-us', 'Production': 'west-eu'}
```

A dictionary comprehension can be arbitrarily complex:

```python
envs = [
    ("Development", "west-us", 27134),
    ("Staging", "east-us", 48628),
    ("Production", "west-eu", 78951),
]

d = {env[0]: env[1].upper() for env in envs if 'us' in env[1]}
print(d)
# {'Development': 'WEST-US', 'Staging': 'EAST-US'}
```

It can also be useful to combine dictionary comprehensions with _list comprehensions_ when constructing a collection of dictionaries.

```python
envs = [
    ("Development", "west-us", 27134),
    ("Staging", "east-us", 48628),
    ("Production", "west-eu", 78951),
]

d = [{"environment": {"type": env[0], "cluster": env[1], "requests": env[2]}} for env in envs]
print(d)
# [
#  {'environment': {'type': 'Development', 'cluster': 'west-us', 'requests': 27134}},
#  {'environment': {'type': 'Staging', 'cluster': 'east-us', 'requests': 48628}},
#  {'environment': {'type': 'Production', 'cluster': 'west-eu', 'requests': 78951}},
# ]
```

In order to create a list, we've used the list comprehension which is a very powerful technique for constructing structures based on some other data structure in a single line.

## Set comprehensions and set theory operations

You can think of sets as of dictionaries of keys with no values. A set can contain only unique values which makes it suitable for all kinds of tasks, for example, deleting duplicates in a list. Sets are also very handy for any kind of data comparison operations such as comparing values of a collection when order and duplication of values don't matter. Sets are created using the `set(iterable)` expression.

```python
input_values = [1, 2, 3, 3, 4, 4, 4, 5]
print(set(input_values))
# {1, 2, 3, 4, 5}
```

A *set comprehension* created by using the `{}` curly brackets, or braces, could be used to get only unique values out of some data collection without constructing a list first:

```python
envs = [
    ("Development", "west-us", 27134),
    ("Staging1", "east-us", 48628),
    ("Staging2", "east-us", 31456),
    ("Production", "west-eu", 78951),
]
clusters = {env[1] for env in envs}
print(clusters)
# {'west-us', 'west-eu', 'east-us'}
```

[Set theory](https://en.wikipedia.org/wiki/Set_theory) is a branch of mathematics that provides logic for working with sets. It defines certain rules that make it possible to perform all kinds of logical operations between two sets:

* intersection: find items that are common to both sets
* symmetric difference: find items that are either in the first or in the second set, but not in both sets
* union: get all items in both sets and add them into a single set with no duplicates
* difference: find items that are in the first set, but not in the second set

```python
# intersection
list1 = ['Development', 'Staging', 'Production']
list2 = ['Development', 'Staging', 'Blue', 'Green']
print(set(list1) & set(list2))
# {'Development', 'Staging'}

# symmetric difference
list1 = ['Development', 'Staging', 'Production']
list2 = ['Development', 'Staging', 'Blue', 'Green']
print set(list1) ^ set(list2)
# {'Production', 'Green', 'Blue'}

# union
list1 = ['Development', 'Staging', 'Production']
list2 = ['Development', 'Staging', 'Blue', 'Green']
print set(list1) | set(list2)
# {'Production', 'Development', 'Blue', 'Green', 'Staging'}

# difference
list1 = ['Development', 'Staging', 'Blue', 'Green']
list2 = ['Development', 'Staging']
print(set(list1) - set(list2))
# {'Green', 'Blue'}
```

However, many other operations such as searching whether a list is a part of another list (that is, a list is a *sublist* of another list) can be easily done with a plain list comprehension:

```python
inventory = ['Development', 'Staging', 'Blue', 'Green']
demand = ['Development', 'Staging', 'Production']

# finding common items
print([item for item in inventory if item in demand])
# ['Development', 'Staging']

# finding items unique to inventory
print([item for item in inventory if item not in demand])
# ['Blue', 'Green']
```

## Enumerated sequences

At some point of time, you may work with a collection of items and you may need to pair each of the item with its index. The index may need to start at some arbitrary number and increase as you work your way up. A simple way to do that would be to use a counter variable. This may be required to have when inserting rows into a database table or for any other operation that would require having a unique identifier for each of the items.

```python
states = ['UNKNOWN', 'ACTIVE', 'DEPRECATED']
count = 10
states_indexed = []

for state in states:
    states_indexed.append((count, state))
    count += 1

print(states_indexed)
# [(10, 'UNKNOWN'), (11, 'ACTIVE'), (12, 'DEPRECATED')]
```

A more elegant solution to this would be to use a built-in function `enumerate()` that does exactly that.


```python
states = ['UNKNOWN', 'ACTIVE', 'DEPRECATED']
print([(index, state) for index, state in enumerate(states, start=10)])
# [(10, 'UNKNOWN'), (11, 'ACTIVE'), (12, 'DEPRECATED')]
```

Happy structuring!
