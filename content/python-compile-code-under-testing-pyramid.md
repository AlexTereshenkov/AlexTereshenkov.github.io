title: Compiling Python code: testing pyramid foundation
date: 2022-05-08
modified: 2022-05-08
author: Alexey Tereshenkov
tags: python
slug: python-compiling-code-base-testing-pyramid
category: python

[TOC]

## Overview

If you start working on a legacy project, you often want to start by understanding how "runnable" code is. If the project has tests, you are lucky and can start by reading the tests code and running them carefully (potentially in a sandbox environment if the tests may have side effects such as connecting to a production database and deleting tables). If the project doesn't have any tests (or there are ones for certain segments only), it may be helpful to see whether the code compiles at all. This is an approach one would normally take for a compiled language such as Java -- if you got an open-source project, for instance, it's common to ask yourself -- does this project build at all?

Because Python is not a compiled language (in the same sense as Java or C++ are), your options to check for project sanity are quite limited. You may want to run some code quality and [static program analysis](https://en.wikipedia.org/wiki/Static_program_analysis) tools, but they may not give you the most accurate picture. In contrast to static code analysis, you may also employ [dynamic program analysis](https://en.wikipedia.org/wiki/Dynamic_program_analysis) and there a [few Python tools](https://github.com/analysis-tools-dev/dynamic-analysis#python) worth taking a look. A very basic approach to start with, however, is to see whether the project files are syntactically correct.

## Compiling Python code

To verify that Python module contains syntactically valid code, you can use the [`compileall`](https://docs.python.org/3/library/compileall.html) module which can be used both from a command line and in Python programs. The `compileall` tool will compile your source code into bytecode files (`.pyc` files in the ``__pycache__` directories) and if there are any syntax errors, the compilation will fail reporting the problem.

Having these pieces of code in a Python module:

    :::python
    def hello(name: str):
        print("Hello " + name)
        print(foobar)

    hello("user")



    class User:

        def __init__(self):
            self.uid = 0

        def greet(self):
            print("Hello!")
            print(self.uid)
            print(self.foobar)

    user = User()
    user.greet()


and running the `compileall` on the directory containing the file above:

    :::bash
    $ python3 -m compileall projectdir
    Listing 'projectdir'...
    Compiling 'projectdir/main.py'...

You may be surprised, but the compilation succeeds. The file above is syntactically correct, even though you may have noticed that `foobar` variable/attribute is undefined; running the program will fail with the `NameError` error (in the function call) and with the `AttributeError` error (in the class instance).

Due to the very dynamic nature of Python (global scope, monkey patching, adding/removing class instance variables), when Python code is compiled into the bytecode, the compiler can't be certain whether the `foobar` variable is accessible in the global scope (introduced by another Python module) or whether `.foobar` attribute will be added at the runtime. 

## Compiling Java code

Java, in contrast, doesn't have the concept of the global scope (in Python sense) and is more conservative in how much can happen at the runtime, so the Java compiler can be of more help:

    :::java
    class User {
    
        private int uid = 0;
        
        public void greet() {
            System.out.println("Hello!");
            System.out.println(this.uid);
            System.out.println(this.foobar);
        }
    }

Running the compiler:

    :::bash
    $ javac main.java
    main.java:8: error: cannot find symbol
        System.out.println(this.foobar);
                            ^
    symbol: variable foobar
    1 error

### Using `compileall` to confirm Python version compatibility

If you start refactoring a legacy project, and you don't have a clear picture whether all Python modules are being exercised when tests are run (you can spot those by looking at a test coverage report after running the tests), you may want to start by fixing any syntax errors (e.g. if you are migrating to Python 3 from Python 2). 

Running `compileall` would also help to confirm that project is compatible with a certain Python version. For example, you have to guarantee compatibility with Python 3.6 and 3.7 and therefore cannot use any new syntax from later versions. Compiling your Python sources into bytecode using a Python interpreter of a certain version is a very cheap way to confirm that the code is compatible.

For instance, you can compile all project code using a particular Python version to make sure it doesn't feature any new syntax you cannot yet support such as [assignment expressions](https://peps.python.org/pep-0572/):

    :::python
    items = [1,2,3,4,5]
    if (n := len(items)) > 3:
        print(f"List is too long (there are {n} items, expected < 3)")

Happy compiling and testing!
