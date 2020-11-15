title: Working with stdout in Python scripts
date: 2020-11-16
modified: 2020-11-16
author: Alexey Tereshenkov
tags: python,logging
slug: working-with-stdout-python
category: python

[TOC]

## Overview

When working with an existing Python script, particularly a legacy script, 
or a script that was supposed to be used once and then thrown away but grew into a business
critical application (yep, this happens), it can be common to see extensive 
usage of `print` or `logging` statements.
Those statements can be spread across the program code and often provide useful information
regarding the status of the process while the script is being executed.

However, if you have been writing a new script and have finished working on it,
or if the script output is not of interest any longer, 
you most likely wouldn't want to clutter the Python console with `print`/`logging` outputs
(particularly if the script is part of another larger pipeline).
However, the information emitted can still be useful to get logged.

## Redirecting to a file

Instead of removing each `print` statement (or switching to `logging.debug` from `logging.info`),
it is possible to specify to what file the `sys.stdout` will redirect writing to.
This will make the `print` and `logging` calls to write to a file on disk instead.

{% include_code python_stdout/program_print.py lang:python :hideall: %}

Now, when running the program, the `print()` calls within the main program logic 
are being redirected to a file on disk.

```text
$ python3 program_print.py
Started script
Finished script
$ cat log.txt 
Getting work done
```

## Redirecting to `StringIO`

It is also possible to use the `io.StringIO()` object to capture everything that will be
written to the `stdout` for the whole script or only a portion of it.

{% include_code python_stdout/program_stringio_var.py lang:python :hideall: %}

Now, when running the program, the `print()` calls within the main program logic 
are being collected into a variable (which is printed here for examination, but can be used
for any custom logging).

```text
$ python3 program_stringio_var.py
Started script
Finished script

Getting work done
```

## Overriding the `sys.stdout.write` method

In both of the examples above, the text that was sent to the original `stdout` wasn't shown
in the console (it's either simply suppressed or captured into a variable).
However, it can be sometimes useful to print the output both to the console _and_ put the output
into a variable.
For this use case, we are essentially after what the `tee` command does in Linux (which can read `stdin` and
then write it to both the `stdout` and to a file).
In Python, this can be achieved by overriding the `sys.stdout.write` method.

{% include_code python_stdout/program_tee.py lang:python :hideall: %}

Now, when running the program, the `print()` calls within the main program logic 
are being collected into a variable (which is printed here for examination, but can be used
for any custom logging).
However, all the `print()` statements are printed as well.

```text
$ python3 program_tee.py
Started script
Getting work done 1
Getting work done 2
Finished script

Getting work done 1
Getting work done 2
```

Happy printing!