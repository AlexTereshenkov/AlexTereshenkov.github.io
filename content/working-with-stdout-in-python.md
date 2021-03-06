title: Working with stdout in Python scripts
date: 2020-11-16
modified: 2020-03-06
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

## Buffering and flushing

When you run a Python program, if the standard output (`stdout`) of its process is redirected 
to some other target (different from your active terminal), then the output of this process will be
buffered into a buffer.
Therefore, output of Python programs that have any text sent to the `stdout` may be buffered and not shown 
until the newline character (`\n`) is sent.

This program won't print anything in your Python console or terminal when being run:

    :::python
    import time 
    for i in range(5): 
        print(i, end=" ") 
        time.sleep(.2) 

In contrast, if there is a `print` call (which by default has the newline character as its 
[`end` parameter](https://docs.python.org/3/library/functions.html#print)), the output will be shown; 
however, all the numbers will be printed at once (not one after another with 0.2 second interval) :

    :::python
    import time 
    for i in range(5): 
        print(i, end=" ") 
        time.sleep(.2) 
    print()

To be able to see each number being printed instead of waiting for the loop 
to complete and see them all at once,
one can change the `stdout` buffering with the [`stdbuf`](https://www.gnu.org/software/coreutils/manual/html_node/stdbuf-invocation.html) utility.
However, the `end` parameter has to be a newline character:

```
$ stdbuf -oL python3 program.py > result.log
```

Alternatively, one can use the `flush` parameter of the `print` function:

    :::python
    import time 
    for i in range(5): 
        print(i, flush=True) 
        time.sleep(2) 

and the call becomes (running `tail -F result.log` will let you see numbers printed in real time):

```
$ python3 std.py > result.log
```

A solution that does not involve flushing is to set the 
[`PYTHONUNBUFFERED`](https://docs.python.org/3/using/cmdline.html#cmdoption-u)
environment variable.
When this environment variable is set, the `stdout` of the Python process will be sent 
to the active terminal in real time (which can be useful for tailing any application
logs, particularly inside a Docker container).

The same effect can also be achieved by passing the `-u` parameter:

```
$ python3 -u std.py > result.log
```

Happy printing!