title: Using quicktype.io service to create Python interfaces from JSON
date: 2020-08-12
modified: 2020-08-12
author: Alexey Tereshenkov
tags: python,json,REST,Swagger
slug: quicktype-json-class-generation
category: python

[TOC]

### Introduction

For the last few years I had to write a few simple Python wrappers around a couple of external services.
There are many advantages to having a nice Pythonic interface into libraries 
and tools that are written in other programming languages.
It often makes it easier to automate, more pleasant to interact with, and faster to program in general.

### Bindings and wrappers

Some wrappers simply expose the original interfaces without adding anything -- these are plain bindings
and this is often the case for C++ libraries that have Python bindings such `Qt` with `PyQt`.
Python code you'd write using plain Python bindings may not feel very Pythonic (due to `camelCase`) 
and because you often have to write programs using other, non-Pythonic, paradigms such 
as `obj.setColor('Red')` instead of `obj.color = 'Red'`.
It is, in fact, not uncommon to write Python wrappers around Python bindings for C++ libraries simply because
the Python bindings do not make Python developers who use them much more productive.

Another group of Python wrapping effort exists around wrapping web services interaction to avoid dealing with
cumbersome HTTP requests construction, response processing, and service communication.
Likewise, wrapping a CLI tool in Python can be very useful if this is the only way to interact with the underlying software.

### Working with JSON

No matter how you are getting back a JSON response -- from a web service or from a CLI tool -- 
you will need to process it to either present the result to the end user or to manage it in some other way.
When dealing with JSON data, the built-in `json` module comes in handy and extracting the information you
need out of a JSON object is trivial.
You could also take advantage of higher level HTTP communication library such as `requests`.

At the beginning, the code may look something like this:

{% include_code quicktype-json-class-generation-basic.py lang:python :hideall: Basic wrapping %}

Output:

    :::text
    Status: All Systems Operational
    Updated at: 2020-08-12T08:08:25.828Z

Interacting with the returned JSON objects using only the `json` module will suffice for smaller scripts
and ad-hoc web service interrogation.
If you'd like to build a Python wrapper around a large REST interface with many endpoints, however,
it may be useful to think about having higher level abstractions for the data entities you deal with.

The code snippet above has a number of issues:

* it relies on having the data elements present when using accessing JSON objects 
(you could work around it using the `.get()` method -- `data.get('status', {}).get('description', 'N/A')` but it is still very fragile)

* as JSON objects keys are represented as strings, it's impossible to run any static type checker 
(and it has additional complications -- refactoring becomes really hard)

* it makes it hard to reason about the data entities as their data type is not obvious 
(and you would have to provide a type hint for each JSON object such as `status: Dict[str, str] = data['status']` which will become tedious very quickly)

### Representation of JSON as Python classes

To make it easier to interact with JSON objects, they can be used to construct instances of Python classes
which are much easier to work with: they provide nice abstraction, they are easy to write unit tests for,
and the code that uses them can be inspected with a static analysis tool such as `mypy`.

{% include_code quicktype-json-class-generation-advanced.py lang:python :hideall: %}

Output:

    :::text
    Status: All Systems Operational
    Updated at: 2020-08-12T08:08:25.828Z

Having these classes will solve the issues that the original code snippet had.
You can now extend the classes with more fields and add additional logic 
to any class -- the `Page` class can have a local time zone property or the 
`Status.description` can be an instance of the `StatusType(Enum)` class, for instance.

### Autogeneration of Python classes from JSON

It would be very useful if one could generate Python classes declarations from an API
specification file.
[Swagger tools](https://swagger.io/docs/swagger-inspector/how-to-create-an-openapi-definition-using-swagger/)
make it possible to generate an API specification which one could then convert into a collection
of Python classes.
This approach is very useful but the generated Python classes would be simply data classes without
any logic -- your fields with the date would be strings, not `datetime` objects.
I think it works best for APIs that change often, during the development when you are iterating
on the API design, or when having the raw data classes is sufficient.

Another approach is to auto-generate a collection of Python classes from the API specification 
and extend their initialization logic and to add additional fields/methods as required.
This approach has worked well for me and would be particularly useful for any internal tooling
when you have control over the API changes.

I found the [QuickType.io](https://app.quicktype.io/) -- the service that can convert JSON into
typesafe code in many languages including Python -- to be really helpful.
The classes declared in the snippet above have been generated by `quicktype.io` from JSON and
then modified so that the root class `System` will have other class instances as its fields.
That is, you just have to provide the root JSON object and the root class `System` will populate
all its fields with respective classes as required.
For this, a handy Python feature of 
[unpacking keyword arguments](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists) 
with `**` is used.

This way, the `quicktype.io` service generates all the boilerplate Python code needed 
and then some additional modification can be done (e.g. to overload the `__repr__` magic 
method to dump a JSON representation of the class instance).
I think you will see the value of using a Python class to represent a JSON object very quickly and
with the help of `quicktype.io`, autogeneration of Python data classes is incredibly easy.

Happy automating!
