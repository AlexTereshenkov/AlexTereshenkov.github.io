title: Using pyfakefs for unit testing in Python
date: 2020-09-01
modified: 2020-09-01
author: Alexey Tereshenkov
tags: python,pyfakefs,pytest,unittest,testing
slug: intro-pyfakefs-python-testing
category: python

[TOC]

### Overview of unit testing

When writing unit tests for programs, it is commonly considered to be a good practice 
to avoid relying on any part of the system infrastructure such as:

* network connectivity (you can't get data from a web service)
* operating system functionality (you can't call `grep`)
* additional software installations (you can't rely on having `Microsoft Excel` installed)

Another suggestion is to avoid making modifications to the files on disk.
Testing pieces of code where files may be created or modified often involves patching
the functions responsible for writing on disk such as the built-in `open` function,
various `os` module functions such as `os.mkdir` and `os.makedirs`, and `pathlib.Path` methods
such as `Path.touch` and `Path.open`.

If writing to file system doesn't happen very often, using a few simple patches will suffice.
However, for more heavy data-driven programs or programs that are written for any kind of 
data processing, patching endless number of function calls throughout the code can become
rather tedious very soon.

### Using system temp directory

At some point, it may be more efficient to use a more relaxed approach which involves using
the `tempfile` module to create and modify files within the operating system temporary directory
which is guaranteed to exist and be writable (at least on POSIX).

This approach has some limitations:

* one wouldn't be able to make changes to files at system paths 
if this is an essential part of the program functionality
* unit tests writing on disk will become slower and with many of them can slow down the
development-testing iterative cycle
* running tests in parallel (or using multithreading) can be unreliable as multiple tests
may attempt to write/read to/from the very same files at the same time
* running a test making file system modifications can leave the system in a favourable state
for the subsequent tests to be run which can lead to flaky tests 

### Using virtual file system

Alternatively, a more robust approach is to not write on disk 
and instead use a virtual, in-memory file system.
For Python, there is a package called [`pyfakefs`](http://jmcgeheeiv.github.io/pyfakefs/release/index.html)
that makes it possible.
Surprisingly it's not very well known in the Python community 
and I thought it would be helpful to share the word as I find this package to be indispensable
in unit testing of programs which work heavily with files.

The package can be used both with `unittest` and `pytest` frameworks and under any operating system.
Here is a trivial example of writing a unit test for a function that merges content of all files
within a given directory into a new file in the same directory.

{% include_code fakefs/test_utils.py lang:python :hideall: %}

Please refer to the `pyfakefs` documentation to learn more.

### Virtual file system caveats

A few notes that can help to avoid common pitfalls:

* make sure not to construct `Path` objects outside of the patching context 
(the `FakeFileSystem()` in the example above) because it will otherwise be pointing to
the real file system since the `Path` class has not been patched yet
* when using the fake file system for integration tests, keep in mind that
you won't be able to use any external tools such as `file` or `cp` commands to interact
with the fake file system files
* to verify that you are using the virtual, fake file system in your tests,
you can choose to create files in a directory
where you won't have modify permissions on your real file system -- this will
help you identify any cases where `pyfakefs` support is limited
* watch closely the permissions the user running the tests have 
as `pyfakefs` will operate under the `root` if run in a Docker container
* do not use the operating system temporary directory as the fake file system
destination directory because [`pyfakefs` doesn't patch the `tempfile` module](http://jmcgeheeiv.github.io/pyfakefs/release/usage.html#os-temporary-directories)

Happy faking!