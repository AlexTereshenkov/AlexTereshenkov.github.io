title: Introduction to QL with Python
date: 2019-07-09
modified: 2022-02-05
author: Alexey Tereshenkov
tags: python,QL
slug: introduction-to-ql-with-python
category: QL

[TOC]

> This is one of the few posts I wrote in 2019 when working for Semmle (later acquired by GitHub) that was originally published on the Semmle blog that was transformed. Python library for QL has changed quite a bit since then, however, many principles are still relevant and helpful for anyone who would want to learn more about QL. See [CodeQL for Python](https://codeql.github.com/docs/codeql-language-guides/codeql-for-python/) to learn more.

## Overview

In this tutorial, you'll learn how to use QL to query a Python codebase and learn how to gain knowledge about tests present in your Python project.

We'll be using QL to analyze the source code of the popular cli tool [click](https://github.com/pallets/click)
by writing [metric queries](https://help.semmle.com/QL/learn-ql/ql/writing-queries/introduction-to-queries.html)
to compute some useful statistics about the code.
The queries posted in this tutorial can be executed using the [LGTM.com query console](https://lgtm.com/query/projects:116307598/lang:python/), 
however, it's also possible to run the queries locally using Eclipse.
Visit [Running queries in your IDE](https://lgtm.com/help/lgtm/running-queries-ide) to learn more.

## QL query components

If you read the [Semmle Introduction to QL](https://help.semmle.com/QL/learn-ql/ql/introduction-to-ql.html),
you will see how QL queries consist of 3 main clauses:

* `from`
* `where`
* `select`

In the `from` clause, you define the objects you would like to run queries against.
For example, here's a query to find all functions in a project:

```ql
from Function f
select f
```

Behind these objects, there are actually database tables that are [generated in QL's extraction process](https://lgtm.com/help/lgtm/generate-database). 
The database consists of dozens of tables, each of which represents a certain object type such as modules or functions.

> Dive in: to see what objects you can add to a `from` clause,
> check out
> [the most commonly used standard QL library classes](https://help.semmle.com/QL/learn-ql/ql/python/introduce-libraries-python.html#summary).

The `where` clause is optional,
and in here you define restrictions on the values that the variables declared in the `from` clause can hold.
For instance, you would need to use the `where` clause if you want to list all Python modules in the repository you analyze that have names starting with `_` 
or find all functions with more than 10 parameters.

For instance, while

```ql
from Function f
select f
```

selects all functions in the project,

```ql
from Function f
where count(f.getAnArg()) > 10
select f
```

selects only those functions that take more than ten arguments.

The `select` clause lets you define what you would like to get back as the result of a QL query execution.
The results are returned as a table where each row represents a single result.
So for example, instead of just printing the names of all the functions 
that take more than 10 parameters, 
you could print the number of parameters as well:

```ql
from Function f
where count(f.getAnArg()) > 10
select f, count(f.getAnArg())
```

As another example, here's a query 
that gets a list of all Python modules available in the source code repository.
We select a module object and a constant string. 

```ql
import python

from Module m
select m, "A module"
```

In the next QL query, we are getting a list of Python modules 
that have names starting with a single underscore 
(excluding dunder modules such as `__init__.py` which start with a double underscore).

```ql
---
queryConsole: https://lgtm.com/query/7269195673257399800/
---
import python

from Module m
where m.getFile().getBaseName().regexpMatch("_[^_].*")
select m, "A private module"
```

You may have noticed that variable `m` 
(which is of the type `Module`) 
has the `getFile` method associated with it.
We can then call the `getBaseName` method,
which returns a string.
Strings have their own built-in methods such as `regexpMatch`,
which can match a string using a regular expression.
 
 > Dive in: For a full list of methods available on strings,
 > see [Built-ins for string](https://help.semmle.com/QL/ql-spec/language.html#built-ins-for-string).
 
You can see what methods and properties each of the built-in types have in the [QL Specification document](https://help.semmle.com/QL/ql-spec/language.html#built-ins).
Having these methods on the `Module` object makes it possible to interrogate database tables using concepts that are more abstract and intuitive to programmers.
This means you can avoid directly dealing with the raw underlying tables of the database.

## Finding test modules

We are interested in learning more about the tests in a Python project,
so let's first find out how many test modules are present in the repo.
The standard Python naming convention is for test modules to begin with `test_`.
We can find these modules by using the `matches()` string method 
which matches strings in the same way as the `LIKE` operator in SQL.

```ql
---
queryConsole: https://lgtm.com/query/8969473391628017193/
---
import python

from Module m
where m.getFile().getBaseName().matches("test\\_%")
select m, "A test module"
```

Another requirement we have to meet 
is that all test modules in the project are located within a single directory named `tests`. 
This is because there can potentially be regular Python modules stored in some directory 
that just happen to have a name starting with `test_`, e.g., `test_db_connection.py` 
(presumably providing means to verify that the connection to a database could be established). 
This module may be used as a part of the application business logic,
and is not a test module, as it won't contain any tests.
In this case, refining the current query doesn't change the query results
but it's good practice anyway 
because it makes the query results more stable, 
if for example, a `test_db_connection.py` file were to be added to the project later.

In this QL query, we are selecting Python modules 
that are located within the `tests` folder 
and have a name starting with `test_`. 
To access the folder in which a Python module is located, 
we need to get access to the `File` object (because a Python module is just a plain file on disk), 
which in turn is located in some directory (which is a `Folder` object), 
which in turn has a name.

```ql
---
queryConsole: https://lgtm.com/query/8736700387179400714/
---
import python

from Module m
where m.getFile().getParent().getBaseName() = "tests"
    and m.getFile().getBaseName().matches("test\\_%")
select m, "A test module"
```

> Dive in: the `click` repository does not have any nested folders within the `tests` folder. 
> However, getting all test files stored in the `tests` recursively is possible using [Transitive closures](https://help.semmle.com/QL/ql-handbook/recursion.html#transitive-closures).
> To apply the `.getParent()` method recursively, we would need to write `m.getFile().getParent+().getBaseName() = "tests"`.

It's possible to combine multiple condition expressions using the `and` operator.
If, instead your project's test modules were either modules that
had names starting with `test_` **or** were stored within the `tests` folder,
you could use the `or` operator:

```ql
---
queryConsole: https://lgtm.com/query/4860024469296565410/
---
import python

from Module m
where m.getFile().getParent().getBaseName() = "tests"
    or m.getFile().getBaseName().matches("test\\_%")
select m, "A test module"
```

## Refactoring QL queries

At this point, as we have identified the test modules in our project, 
we can start learning more about the actual tests. 
However, as our query gets bigger, 
it makes sense to refactor some of its parts into separate entities
which could be reused by multiple queries.
This often has the added benefit of making the query easier to read.

In QL, a [predicate](https://help.semmle.com/QL/ql-handbook/predicates.html) can be used for this. 
In this QL query, we'll be using a [predicate without result](https://help.semmle.com/QL/ql-handbook/predicates.html#predicates-without-result). 
You can think of these types of predicates as boolean functions.
In the following predicate, we pass in an argument `m` that has the type `Module`.
The predicate's body has an expression 
that is evaluated and keeps only the modules for which the condition holds. 

This QL predicate would keep only those Python modules that are located within the `tests` folder. 

```ql
predicate isInsideTestsFolder(Module m) {
    m.getFile().getParent().getBaseName() = "tests"
}
```

To use a predicate within a QL query, 
you would put a predicate call in the `where` clause:

```ql
---
queryConsole: https://lgtm.com/query/2694103716087854413/
---
import python

predicate isInsideTestsFolder(Module m) {
    m.getFile().getParent().getBaseName() = "tests"
}

from Module m
where isInsideTestsFolder(m)
select m, "A module inside tests folder"
```

A predicate, just like any function, can have multiple parameters. 
For instance, if we want to have a more generic predicate 
that would keep modules located within any given folder, 
we would need to add a second parameter. 
This makes a predicate more flexible,
as we can reuse this predicate in other queries passing in the name of directories with test modules 
when analyzing other Python repositories.

```ql
---
queryConsole: https://lgtm.com/query/7407075760043821247/
---
import python

predicate isInsideFolder(Module m, string folderName) {
    m.getFile().getParent().getBaseName() = folderName
}

from Module m
where isInsideFolder(m, "tests")
select m, "A module inside the tests folder"
```

> Dive in: The `folderName` object is of `string` type. QL supports multiple primitive types: `boolean`, `date`, `float`, `int`, and `string`. 
> To learn more about these types, visit [Kinds of types](https://help.semmle.com/QL/ql-spec/language.html#kinds-of-types).

A QL query can contain many predicates. 
In this QL query, we have extracted the functionality of matching a test module by name into the predicate `nameMatchesTestPattern`.

```ql
---
queryConsole: https://lgtm.com/query/6256521983311323313/
---
import python

predicate isInsideFolder(Module m, string folderName) {
    m.getFile().getParent().getBaseName() = folderName
}

predicate nameMatchesTestPattern(Module m) {    
    m.getFile().getBaseName().matches("test\\_%")
}

from Module m
where isInsideFolder(m, "tests") and nameMatchesTestPattern(m)
select m, "A test module"
```

## Count number of tests per file

Now that we have found all the test modules, and have modularized our code a bit,
we are ready to collect some metrics about this project's test code. 
It can be helpful to know how many tests are defined in each test module; 
having too many tests in a single module can indicate 
that it's testing too many pieces of the application 
and that there's potential for refactoring. 
If a module has just one or two tests, perhaps more tests could be added.

The project we are exploring uses `pytest` for its test framework, meaning 
that each test that will be run is defined as a Python function named `test_%name%`,
where `%name%` describes what this particular test does. 
This means we have to count the number of functions 
that have names starting with `test_` defined in each test module.

In order to interact with functions, you have to use the `Function` object.
In the following QL predicate, 
we count the number of test functions in the module 
that is passed in as an input parameter. 

We can also write predicates that compute values derived from their parameters. 
Such predicates are called [predicates with results](https://help.semmle.com/QL/ql-handbook/predicates.html#predicates-with-result).
For a QL predicate to return a value, it needs to be given a return type
(in this instance `int`),
and the special variable `result` needs to be bound to something of that same type,
(in this case, we bind it to the result of a call to `count`).

```ql
int getTestsCount(Module m) {
    result = count(Function f |
        f.getEnclosingModule() = m and f.getName().matches("test\\_%")
        | f)
}
```

Using the `count` aggregate requires having a special syntax:

1. We define the variables we would like to use; in this case, we are using a single variable of type `Function` named `f`.
2. We define what condition should hold using an expression; 
only functions that are defined in the scope of a given module would be kept (`f.getEnclosingModule()` method does the work) 
and function names should start with `test_` (`f.getName().matches()` method does the work).
3. We define what the `count` aggregate exactly counts;
since we are interested in the number of functions that meet our condition, we simply count `f`.

> Dive in: Visit [Aggregates](https://help.semmle.com/QL/ql-spec/language.html#aggregations) to learn more about `count` and other QL aggregates such as `max` and `sum`.

We can now use this predicate within the QL query:
    
```ql
---
queryConsole: https://lgtm.com/query/8228699770073082994/
---
import python

predicate isInsideFolder(Module m, string folderName) {
    m.getFile().getParent().getBaseName() = folderName
}

predicate nameMatchesTestPattern(Module m) {
    m.getFile().getBaseName().matches("test\\_%")
}

int getTestsCount(Module m) {
    result = count(Function f |
        f.getEnclosingModule() = m
        and f.getName().matches("test\\_%")
        | f)
}

from Module m, Folder f
where isInsideFolder(m, "tests")
    and nameMatchesTestPattern(m)

select m, m.getFile().getBaseName(), getTestsCount(m) as TestCount
order by TestCount
```

To include the number of tests in the output results, 
we have extended the `select` statement with another column aliased `TestCount` ,
that represents the result of the `getTestsCount(m)` predicate call. 
It would be helpful to see the test modules with the fewest tests in them 
which is why we use the `order by` command 
that sorts the results in ascending order by `TestCount`.

## Find Python modules without a corresponding test module

Being able to detect modules 
that do not have corresponding test modules can be helpful, for example
when there is a policy within the development team 
which dictates that each Python module should have an associated test module.

Since we already know how to find test modules, 
we need only find the
modules that don't have a corresponding test module. 
In other words, if for the `read_file.py` module there is no `tests/test_read_file.py` module, 
we can conclude that this module does not have any tests (or that it has been named without following the Python convention).

To find out whether a program module has a corresponding test module, 
we need to create a new predicate 
that finds only those program modules 
which don't have a paired test module.

```ql
predicate moduleWithoutTests(Module m, Folder f) {
    not exists(
        f.getFile("test_" + m.getFile().getBaseName())
    )
    and
    not exists(
        f.getFile("test" + m.getFile().getBaseName())
    )
}
```

As you can see, a predicate can have one or more input parameters. 
The reason we pass a `Folder` is because we want to specify 
where the test modules are stored. 
The logic that is being evaluated in this predicate is rather simple;
having a passed module as a parameter, say `%name%.py`,
it checks whether there is a file named `test_%name%.py`. 
This can be done using a special `exists` aggregate 
which would hold if there is a test module in the given folder.
We also have to look for modules that start with `test` to support private modules
that, by convention, start with a single underscore (`_`).

```ql
---
queryConsole: https://lgtm.com/query/4650679191588923532/
---
import python

predicate isInsideFolder(Module m, string folderName) {
    m.getFile().getParent().getBaseName() = folderName
}

predicate nameMatchesTestPattern(Module m) {
    m.getFile().getBaseName().matches("test\\_%")
}

predicate moduleWithoutTests(Module m, Folder f) {
    not exists(
        f.getFile("test_" + m.getFile().getBaseName())
    )
    and
    not exists(
        f.getFile("test" + m.getFile().getBaseName())
    )
}

from Module m, Folder f
where isInsideFolder(m, "click")
    and moduleWithoutTests(m, f.getFolder("tests"))

select m, m.getFile().getBaseName()
```

In this query, we have analyzed modules from the `click` folder only. 
It's common to restrict such queries to the main code of a project, since a Python project can have utility modules 
used for documentation generation or raw data storage,
for which presence of tests may not be necessary.

## Creating a QL library

As you may have noticed, we have defined quite a few useful predicates. 
They all have something in common—they are applicable to test modules. 
Our query has gotten fairly big, but the actual `select` statement is rather small.

To keep the query tidy and to improve modularization, 
we can create a `TestModule` class 
that will be a subclass of the standard QL class `Module`. 
This class could be stored in a separate QL library file (`.qll`),
which could then be imported in any other query that deals with test modules.

> Dive in: learn more about [defining a class](https://help.semmle.com/QL/ql-handbook/types.html#defining-a-class).

If you want to run the queries locally in Eclipse, 
you can put this code into a new QL library file `Testing.qll` 
so it can be used in query files (`.ql` files).

```ql
import python

string getTestPrefix() { result = "test\\_%" }
string getTestsFolder() { result = "tests" }

/** Keeps modules located within the given folder. */
private predicate isInsideFolder(Module m) {
    m.getFile().getParent().getBaseName() = getTestsFolder()
}

/** Keeps modules that have names starting with the defined prefix. */
private predicate nameMatchesTestPattern(Module m) {    
    m.getFile().getBaseName().matches(getTestPrefix())
}

class TestModule extends Module {    
    TestModule() { isInsideFolder(this) and nameMatchesTestPattern(this) }
    
    /** Gets count of functions within the module which 
    name starts with the defined prefix. */
    int getTestsCount() {       
        result = count(Function f | 
            f.getEnclosingModule() = this
            and f.getName().matches(getTestPrefix())
            | f)
    }
}
```

Alternatively, if you are using LGTM.com, 
then you can define the class along with the actual query:

```ql
---
queryConsole: https://lgtm.com/query/4740785288826699608/
---
import python

string getTestPrefix() { result = "test\\_%" }
string getTestsFolder() { result = "tests" }

/** Keeps modules located within the given folder. */
private predicate isInsideFolder(Module m) {
    m.getFile().getParent().getBaseName() = getTestsFolder()
}

/** Keeps modules that have names starting with the defined prefix. */
private predicate nameMatchesTestPattern(Module m) {    
    m.getFile().getBaseName().matches(getTestPrefix())
}

class TestModule extends Module {    
    TestModule() { isInsideFolder(this) and nameMatchesTestPattern(this) }
    
    /** Gets count of functions within the module 
    which name starts with the defined prefix. */
    int getTestsCount() {       
        result = count(Function f | 
            f.getEnclosingModule() = this
            and f.getName().matches(getTestPrefix())
            | f)
    }
}

from TestModule tm
select tm, tm.getTestsCount() as TestCount
order by TestCount desc
```

As we have used string `"test\\_%"` in a few places, 
it can be useful to pull it into a variable. 
Using [fields in classes](https://help.semmle.com/QL/ql-handbook/types.html#fields) is an advanced topic, 
so instead, for now we've simply used a predicate with result
that just gives us back this string.
This means we would need to define the test prefix only within this predicate 
and not within multiple predicates.

To keep this class in a separate file, 
you would need to use the QL for Eclipse plugin to run queries locally on your machine.
We would need then to import the library 
and then use the `TestModule` class instead of the built-in `Module` class we have used before.

```ql
import python
import Testing

from TestModule tm
select tm, tm.getTestsCount() as TestCount
order by TestCount desc
```

This is the end of this tutorial.
I hope you enjoy trying out QL on your own projects!
If you have any questions,
don't hesitate to ask on [the community forum](https://discuss.lgtm.com/).

Happy Querying!