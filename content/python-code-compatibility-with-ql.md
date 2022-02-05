title: Finding Python code compatibility issues with QL
date: 2019-08-13
modified: 2022-02-05
author: Alexey Tereshenkov
tags: python,QL
slug: finding-python-compatibility-issues-with-ql
category: QL

[TOC]

> This is one of the few posts I wrote in 2019 when working for Semmle (later acquired by GitHub) that was originally published on the Semmle blog that was transformed. Python library for QL has changed quite a bit since then, however, many principles are still relevant and helpful for anyone who would want to learn more about QL. See [CodeQL for Python](https://codeql.github.com/docs/codeql-language-guides/codeql-for-python/) to learn more.

# Overview

In this tutorial, you'll learn how to use QL to query a Python codebase 
and learn how to check for Python 2/3 compatibility. 
We'll be writing [alert queries](https://help.semmle.com/QL/learn-ql/ql/writing-queries/introduction-to-queries.html), 
that is, queries that highlight issues in specific locations in your code. 
The tutorial assumes that you're familiar with the basics of QL for Python. 
If not, you might want to read my previous post ([Introducing the QL libraries for Python](https://blog.semmle.com/python-code-analysis-ql/)).

## Python 2 and 3

As the official end of life of Python 2 approaches, 
more and more Python projects are being converted from Python 2 to Python 3.
The majority of infrastructure projects are now on Python 3, and many are Python 3 only.
At some point, you will likely need to upgrade your project.
There are myriads of useful resources 
that can help you upgrade your project's codebase. 
There are tools that can upgrade code in a semi-automatic fashion; 
there are linters and static code analysis tools 
that will help you spot code that's not compatible with Python 3. 
There are also quite a few documents 
to help you learn what's new in Python 3 
and avoid the common pitfalls when you upgrade.

To learn more, 
visit the main [What’s New In Python 3.0](https://docs.python.org/3/whatsnew/3.0.html) reference page. 
To learn how to write code that's compatible with both Python 2 and Python 3, 
visit [Python-Future](https://python-future.org/).

Upgrading a codebase to Python 3, or supporting both Python 2 and 3, can be a challenge. 
The Python 2 interpreter reports a `SyntaxError` for some of the new syntax features in Python 3. 
Some Python 2 features aren't available in Python 3, 
so when the Python 3 interpreter encounters them 
it raises a runtime error 
or gives a different result.

For instance, the `print` statement was replaced by the `print()` function 
so running a module with a `print` statement under Python 3 
will cause a `SyntaxError`. 
Using the `print` statement as if it were a function in Python 2, 
however, won't raise a `SyntaxError`, but its behavior will be different:

* Python 3

```python
>>> print("value1", "value2")
value1 value2
```

* Python 2

```python
>>> print("value1", "value2")
('value1', 'value2')
```

In contrast, the `long` type was removed in Python 3 
leaving only one built-in integer type named `int`. 
Hence, trying to use the `long` keyword in a module executed 
by a Python 3 interpreter, will cause a `NameError` at runtime:

* Python 3

```python
>>> isinstance(5, int)
True

>>> isinstance(5, long)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
NameError: name 'long' is not defined
```

## Using QL

A series of QL queries is shown below, 
highlighting some of the issues found 
when working with Python 2 and 3 compatibility.
We explain how the queries work 
so you can learn how to use the QL libraries for Python,
which will help you to write your own custom queries.

A Python project can be analyzed using either a Python 2 or a Python 3 interpreter. 
To learn more, read [How is the Python version identified?](https://lgtm.com/help/lgtm/analysis-faqs#how-python-version-identified) on LGTM.com.

Analysis run on LGTM will spot common errors using built-in queries. 
To find out which version of Python was used to analyze a codebase, 
you can use the built-in `major_version` and `minor_version` predicates:

```ql
import python
select major_version(), minor_version()
```

These predicates will come in handy later on 
when we will be trying to find issues in the code 
that are relevant only for Python 2 or for Python 3.

### Built-in queries

#### Syntax error

Syntax errors are found by the built-in [Syntax error](https://lgtm.com/rules/4860085/) query. 
They prevent a module being evaluated and thus imported. 
An attempt to import a module with invalid syntax will fail; 
a `SyntaxError` will be raised. 
Syntax errors are caused by invalid Python syntax,
for example:

```python
# variables cannot contain any symbol 
# other than a digit, a letter, and an underscore
variable$ = "value"

# attempt to use an invalid increment operator
value = 10
value++

# incorrect usage of lambda
print(lambda x: x += 10)

# invalid inequality test
print(source <> target)
``` 

Note that in Python 2, it's okay to mix tabs and spaces for code indentation. 
However, in Python 3, a new [`TabError`](https://docs.python.org/3/library/exceptions.html#TabError) 
is raised when indentation contains an inconsistent use of tabs and spaces. 
This type of error is also caught by the syntax errors check.

#### Encoding error

Encoding errors are found by the built-in [Encoding error](https://lgtm.com/rules/1814222703/) query.
They prevent a module being evaluated and thus imported. 
An attempt to import a module with an invalid encoding will fail; 
a `SyntaxError` will be raised. 
Note that in Python 2, the default encoding is ASCII.

### Existing custom queries

In addition to the built-in queries that are part of the core LGTM suite, 
there are a few custom queries 
that the community of QL writers has contributed.
I myself wrote a new custom query shortly after I joined Semmle 
while I was learning how the QL libraries for Python worked. 
This query, `Use of 'return' or 'yield' outside a function`,
was first published in the [public GitHub QL repository](https://github.com/Semmle/ql/blob/653c8b8496cd0d95e459d1cd7a95083970d37cba/python/ql/src/Statements/ReturnOrYieldOutsideFunction.ql) 
and later became a built-in query that is run on [LGTM.com](https://lgtm.com/rules/1509050896213/).

## Writing new QL queries

### New 'raise from' syntax

[PEP 3109 -- Raising Exceptions in Python 3000](https://www.python.org/dev/peps/pep-3109/) and [PEP 3134 -- Exception Chaining and Embedded Tracebacks](https://www.python.org/dev/peps/pep-3134/) 
introduced new syntax for the raise statement: `raise [expr [from expr]]`. 
The optional `from` clause can be used to chain exceptions. 
When `from` is used, the second expression must be another exception class or instance. 
To learn more, visit [The raise statement](https://docs.python.org/3/reference/simple_stmts.html#raise).

Since version 3.3, you can use `None` to suppress the chained exception, for example:

```python
try:
    value = 1 / 0
except Exception:
    raise Exception() from None
```

However, a project style guide may discourage the suppression of exception chaining using `from None`,
for example, to maintain backwards compatibility. 
If this is the case, you would want to find all such occurrences. 

The QL libraries for Python contain classes that are useful for finding this syntax.
These can be imported and used in a custom QL query. 
The easiest way to find this type of `raise` statement is to use the `Raise` class. 
Using this QL query, we can spot when the `raise from None` syntax is used:

```ql
import python

from Raise r
where r.getCause().getAFlowNode().pointsTo(Value::named("None"))
select r
```

The `.getCause()` method gives us the cause of the `raise` statement 
and it's possible to find out 
what object this cause points to using the `.pointsTo()` method. 
In this case, we test whether this is a `None` object. 

To extend our query, we could check 
whether a valid object is being used in the `from` part. 
The object can be either `None`
or a valid exception class or instance.

For example, this `raise` statement has an invalid object so, 
a `TypeError` with the message, `TypeError: exception causes must derive from BaseException`, 
is raised when it's run:

```python
try:
    print(1 / 0)
except Exception as exc:
    raise RuntimeError("Something happened") from "Program stopped"
```

This QL query will find all `raise ... from ...` statements 
where the `from` object is invalid.

```ql
import python

from Raise r, Value v
where r.getCause().getAFlowNode().pointsTo(v) and
      v != Value::named("None") and
      not v.getClass().getASuperType() = Value::named("BaseException")
select r, v
```

A class instance is a legal exception type 
if it inherits from the `BaseException` class. 
Thus, this query would be able to spot 
when an invalid object type is used in the `raise from` clause.

### Support for unicode in identifier names

In Python 2, only ASCII characters could be used in the names of Python identifiers 
including, but not limited to, variables, functions, and classes. 
Trying to define a variable `café` (e-acute) in Python 2, 
would result in a `SyntaxError: invalid syntax`.

In Python 3, with [PEP 3131 -- Supporting Non-ASCII Identifiers](https://www.python.org/dev/peps/pep-3131/), this limitation was removed 
and now additional characters from outside the ASCII range (see the [docs](https://docs.python.org/3/reference/lexical_analysis.html#identifiers)) 
could be used in identifier names. 
This code is valid in Python 3: 

```python
café = object()
print(café)
```

However, a project style guide may prohibit the use of non-ASCII characters in identifiers
to maintain backwards compatibility. 
To find identifiers that break this rule 
we have to find all identifiers 
that contain characters other than letters, numbers, and the underscore symbol. 
This can be done using a regular expression. 
We don't have to worry about the validity of identifier names; 
a built-in query already finds any syntax errors, 
such as variable names that don't start with an underscore or a letter. 
Since this check is relevant only for Python 3, a condition of `major_version() = 3` is included.
In Python 2 this issue would be caught by the query 
that reports all `SyntaxError` cases.

This QL query finds all non-ASCII Python identifiers.

```ql
import python

from string identifier, AstNode n
where 
    (
    identifier = n.(Name).getId()
    or
    identifier = n.(Attribute).getName()
    ) and not identifier.regexpMatch("[a-zA-Z_][a-zA-Z_0-9]*")
    and major_version() = 3
select n, "Non ASCII character in identifier's name"
```

In this query, the `Name` class represents the names of identifiers. 
The `Attribute` class represents the names of attribute expressions, 
for example, a class method.
We need to use the `AstNode` class to access the location of each identifier in the code. 
However, the `AstNode` class doesn't provide the identifier's name 
as a string that we can test using a regular expression. 
To get the name as a string, we call the member predicates `.getId()` and `.getName()`.
Since these are defined for a more specific type, we need to use a type cast.

> Dive in: This could have been done using postfix and prefix casts. Visit the [Casts](https://help.semmle.com/QL/ql-handbook/expressions.html#casts) help page to learn more.
 
### Comparing objects of different types

In Python 2, objects of different types are ordered by their type names 
(with the exception of numbers). 
This results in behavior 
that can puzzle developers who are unfamiliar with this implementation detail.

* Python 2:

```python
>>> print 50 < "Text"
True

>>> [10, 20] > 'Text' 
False
```

This comparison essentially compares the types of the objects, that is: `'int' < 'str'`. 
This is `True` because the word representing type `int` starts with `i` 
which is smaller than `s` - the `str` type (using lexicographic order). 
Likewise, because `'list' > 'str'` is `False`, 
comparing a list object to a string object would return `False`.  

In Python 3, if you use ordering comparison operators 
when the operands don’t have a natural ordering 
that makes sense, a `TypeError` exception is raised. 
This implies that there can be Python 2 code 
which may compare objects of different types 
and this would not be an issue 
until you run the program with a Python 3 interpreter.

For instance, this valid Python 2 code would fail in Python 3:

```python
data = [10, 20, 30]
mapper = {"Source": "Target"}
print(data > mapper)
print(data < mapper)
```

We can use QL to write a custom query 
that finds comparisons of invalid data types.

```ql
import python

ClassValue orderedType() {
  exists(string typename | result = Value::named(typename) |
    typename = "str" or typename = "float" or typename = "list"
  )
}

from
  CompareNode compare, ControlFlowNode left, ControlFlowNode right, 
  Context ctx, Value lval, Value rval, Cmpop op

where
  compare.operands(left, op, right) and
  (
    op instanceof Lt or
    op instanceof LtE or
    op instanceof Gt or
    op instanceof GtE
  ) and
  left.pointsTo(ctx, lval, _) and
  right.pointsTo(ctx, rval, _) and
  lval.getClass() != rval.getClass() and
  lval.getClass() = orderedType() and
  rval.getClass() = orderedType()

select compare, "Invalid comparison of objects due to type difference"
```

At this point it might be useful to refactor the code above 
because the `where` clause gets too difficult to read.
We can define a helper predicate, `incomparableTypes`, that would hold 
if comparison expressions are of incompatible types:

```ql
import python

predicate incomparableTypes(ClassValue a, ClassValue b) {
    not a = b and 
    a = orderedType() and
    b = orderedType()
}

ClassValue orderedType() {
  exists(string typename | result = Value::named(typename) |
    typename = "str" or typename = "float" or typename = "list"
  )
}

from
  CompareNode compare, ControlFlowNode left, ControlFlowNode right, 
  Context ctx, Value lval, Value rval, Cmpop op

where
  compare.operands(left, op, right) and
  (
    op instanceof Lt or
    op instanceof LtE or
    op instanceof Gt or
    op instanceof GtE
  ) and
  left.pointsTo(ctx, lval, _) and
  right.pointsTo(ctx, rval, _) and
  incomparableTypes(lval, rval)

select compare, "Invalid comparison of objects due to type difference"
```

The `left` and `right` expressions of the comparison can be inspected to check 
what type they point to using the `.pointsTo()` method.
We use the don't care variable `_` to state
that we don't care what kind of `Value` the left and right expressions point to, 
however, they must be of a certain type.

The query above currently only supports comparing strings, floats, and lists. 
However, it is easy to extend it just by copying the relevant `where` section 
and changing the class types. 
For instance, to extend this query to include the comparison of integer objects, 
you would just need to add the following section:

```ql
...
ClassValue orderedType() {
  exists(string typename | result = Value::named(typename) |
    typename = "str" or typename = "float" or 
    typename = "list" or typename = "int"
  )
}
...
```

### Octal literals syntax support 

Octal literals in Python 3 can no longer be defined in the form of a number 
starting with `0`, such as `0562`,
as they could be in Python 2. 
Python 2 has two methods for defining octal literals:

```python
>>> print(0562 == 0o562)
True
```

Python 3 only supports the second of these syntaxes and using `0562` would cause a `SyntaxError`. 
Instead, you need to use a zero followed by a lower or upper case `o` (that is, `o` and `O`),
for example, `0o562` or `0O562` . 
The upper case `O` looks very similar to zero (`0`) 
so using a lowercase `o` may be preferable. 

Therefore, it can be helpful to search for octal literals in Python 2 
that don't use `o` to avoid issues after converting the codebase to Python 3. 
Fortunately, there's already an existing query - [Confusing octal literal](https://lgtm.com/rules/1800090/) - 
which finds octal literals with a leading `0` 
because they can easily be misread as decimal values. 
This query does just what we need.

It's worth bearing in mind that this query doesn't raise alerts for octal literals 
that are of 4, 5, or 7 digits in length. 
These are ignored because Python code may include Unix permission mode octals
which can be safely ignored. 
Here we want to raise an alert for all octal literals, 
so we simply remove the part 
that filters out octals of a certain length. 
This QL query finds all octal literals 
that would raise `SyntaxError` in Python 3:

```ql
import python

predicate is_old_octal(IntegerLiteral i) {
  exists(string text | text = i.getText() |
    text.charAt(0) = "0" and
    not text = "00" and
    text.charAt(_) != "0" and
    exists(text.charAt(1).toInt())
  )
}

from IntegerLiteral i
where major_version() = 3 and is_old_octal(i)
select i, "Invalid octal literal"
```

In this query we take advantage of the `exists` quantifier to define a predicate 
which holds for any integer literal that starts with a zero digit.

> Dive in: Visit the [Explicit quantifiers](https://help.semmle.com/QL/ql-handbook/formulas.html?#exists) help page to learn more about quantifiers in QL.

### Delimiter in numeric literals

Python 3.6 supports using `_` as a delimiter in numeric literals. 
This functionality was introduced in [PEP 515 -- Underscores in Numeric Literals](https://www.python.org/dev/peps/pep-0515/). 
This is an example of how this works in Python 3.6:

```python
>>> 5_000.46 == 5000.46
True

>>> 5_000 + 1_000 == 6000
True
``` 

If your project style guide prohibits using this feature, 
for instance, for consistency with the Python 2 code, 
then you could write a custom QL query 
that would be able to find code where `_` is used in numeric literals. 
Running code with underscores in numeric literals using a Python 2 interpreter 
would raise a `SyntaxError`.

```ql
import python

predicate hasUnderscore(Num n) { 
    exists(int i | n.getText().charAt(i) = "_")
}

string numValue(Num n) {
  result = n.(IntegerLiteral).getValue().toString() or
  result = n.(FloatLiteral).getValue().toString()
}

from Num num
where hasUnderscore(num)
select num, num.getText() as AsInCode, numValue(num) as AsToReader
```

Previously, we've only included two items in the `select` statement, 
however, you can return an arbitrary number of items. 
The `.getText()` method gives the actual source code (for example, `5_000`) 
whereas the `numValue` predicate gives the string representation of the literal 
with underscores removed (for example, `5000`). 
Being able to return multiple items within the `select` statement 
is extremely handy during the debugging and query writing process.

If your project style guide is more relaxed 
and permits having underscores in integers only, 
but prohibits using underscore in floats, 
you can adjust the query to work solely with floats:

```ql
import python

predicate hasUnderscore(Num n) { 
    exists(int i | n.getText().charAt(i) = "_")
}

from Num num
where hasUnderscore(num)
    and not num instanceof IntegerLiteral
select num
```

### Long integer type is not supported by Python 3

With the implementation of [PEP 237 -- Unifying Long Integers and Integers](https://www.python.org/dev/peps/pep-0237/), 
the `long` type was merged with the `int` type. 
This means that having integer literals with `L`, for example, `10560L` in Python 3 
would raise a `SyntaxError` at runtime. 
To spot integers that wouldn't be compatible with Python 3 in your Python 2 project, 
you can use this custom QL query:

```ql
import python

string getLongPostfix() { result = "L" or result = "l" }

from IntegerLiteral num
where num.getText().charAt(num.getText().length() - 1) = getLongPostfix()
select num
```

> Dive in: `.charAt` string method is implemented using [Java `String.charAt`](https://docs.oracle.com/javase/10/docs/api/java/lang/String.html#charAt(int)) 
> and doesn't support negative indexing.

### The 'cmp' parameter for 'sorted(list)' is no longer supported

Running the valid Python 2 code in the example below using a Python 3 interpreter
would result in a `TypeError` 
because `cmp` is no longer a supported keyword argument for the `sorted` function. 
Visit [The Old Way Using the cmp Parameter](https://docs.python.org/3/howto/sorting.html#the-old-way-using-the-cmp-parameter) to learn more.
 
```python
def compare_as_ints(a, b):
    return a - b

sorted([50, 30, 40, 20, 10], cmp=compare_as_ints)
```

To spot this issue in Python code, 
we would need to find all calls to the built-in `sorted` function 
and see if the `cmp` keyword argument is being passed. 
This QL query will find all calls to the `sorted` function 
where the keyword argument `cmp` has been used.

```ql
import python
from CallNode call
where
   Value::named("sorted").getACall() = call and
   exists(call.getArgByName("cmp"))
select call, "Call to sorted built-in function with cmp keyword argument."
```

The `CallNode` class represents all calls in the code. 
We use this because we aren't interested in function definitions 
(which are accessed through the `Function` class) but in function calls. 
Once we've got the `sorted` built-in function, 
it's just a matter of finding `sorted()` calls 
with the `cmp` keyword argument supplied. 
You could reuse this QL query to find other built-in functions 
where the signature varies between Python versions.

### Methods 'dict.iterkeys()', 'dict.iteritems()' and 'dict.itervalues()' are deprecated

An attempt to access any of these dictionary methods 
would raise an `AttributeError` 
when running the code against a Python 3 interpreter:

```python
data = {1: 10, 2: 20}
for k, v in data.iteritems():
    print(k, v)
```

Therefore, we might want to write a QL query 
to spot when those methods access an object of `dict` type.

```ql
import python

string unsupportedDictMethod() {
  result = "iteritems" or
  result = "iterkeys" or
  result = "itervalues"
}

from Attribute attr, Value v
where
  attr.getValue().getAFlowNode().pointsTo(v) and
  v.getClass() = Value::named("dict") and
  attr.getAttr() = unsupportedDictMethod()
select attr, "A deprecated dictionary method was used"
```

As before, the `AstNode` root class gives us access to all elements of the source code. 
The `Attribute` class gives us access to all attributes that are accessed. 
The attribute object is tied to the object 
and this tie can be identified using the `.pointsTo()` method. 
Once we've found all the dictionary attributes throughout the source code, 
we leave only those that are no longer supported 
using a convenience predicate, `unsupportedDictMethod`.

This is the end of this tutorial. 
The queries posted in this post can be executed using the [LGTM.com query console](https://lgtm.com/query/projects:116307598/lang:python/), 
however, it's also possible to run the queries locally using Eclipse. 
Visit [Running queries in your IDE](https://lgtm.com/help/lgtm/running-queries-ide) to learn more.
I hope you enjoy trying out QL on your own projects!
If you have any questions,
don't hesitate to ask on [the community forum](https://discuss.lgtm.com/).

Happy Querying!