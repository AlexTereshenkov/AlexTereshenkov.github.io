title: Running Python tests with tox in a Docker container
date: 2020-11-03
modified: 2020-11-03
author: Alexey Tereshenkov
tags: python,docker,tox,testing
slug: run-python-tests-with-tox-in-docker
category: python

[TOC]

### Overview

When you are working on Python code that is supposed to be running on Python interpreters
of multiple versions (and potentially with multiple versions of 3rd party packages),
to be able to test that your code works and produces expected result you would need
to create isolated virtual environments.
Each of these virtual environments will have a certain version of Python 
and a certain version of each 3rd party package that your programs depend on.
By having just a few versions of Python with a couple of versions of a few packages,
it becomes rather tedious to create and maintain those virtual environments manually very soon.
[`tox`](https://tox.readthedocs.io/en/latest/) is a tool that can help you with this.

### Preparing Python virtual environments

It is possible to create Python virtual environments manually and then let `tox` use
them, however, you would most likely want `tox` to generate those virtual environments
for you.
For `tox` to use Python interpreters of multiple versions, they have to be installed
on your machine.
Even though this is possible, it may still be less optimal given that you will most
likely need to make system changes (install a system package on Linux, use `homebrew` on MacOS,
or download a Python app or an installer on Windows).
Fortunately, `tox` can be run in a Docker container which will help to prevent cluttering your system.

### Running tests with tox in Docker: simple configuration

To be able to run Python tests with `tox` in a Docker container, you will need a Dockerfile.

```Dockerfile
FROM ubuntu:18.04

RUN apt-get -qq update
RUN apt-get install -y --no-install-recommends \
  python3.7 python3.7-distutils python3.7-dev \
  python3.8 python3.8-distutils python3.8-dev \
  wget \
  ca-certificates

RUN wget https://bootstrap.pypa.io/get-pip.py \
  && python3 get-pip.py pip==19.1.1 \
  && rm get-pip.py

RUN python3.6 --version
RUN python3.7 --version
RUN python3.8 --version

RUN pip3 install tox pytest
```

The `tox.ini` file where you specify the Python environments.

```
[tox]
envlist = py36,py37,py38
skipsdist = True

[testenv]
deps = pytest
commands = pytest
```

The `test_module.py` containing a simple test function.

```python
def test_foo():
    assert 2 + 3 == 5
```

Now you can build an image and then run the tests. 

```bash
$ docker build -t snake .
$ docker run -it -v ${PWD}/:/app snake /bin/sh -c 'cd app; tox'
```

The `pytest` output will be printed for each of the Python environments
in which the tests have been run (posted below with some sections removed for brevity).

```
using tox.ini: /app/tox.ini (pid 7)
...
[16] /app$ /app/.tox/py36/bin/pytest
================================================= test session starts =================================================
platform linux -- Python 3.6.9, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py36/.pytest_cache
rootdir: /app
collected 1 item                                                                                                      

test_module.py .                                                                                                [100%]

================================================== 1 passed in 0.01s ==================================================

...
[21] /app$ /app/.tox/py37/bin/pytest
================================================= test session starts =================================================
platform linux -- Python 3.7.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py37/.pytest_cache
rootdir: /app
collected 1 item                                                                                                      

test_module.py .                                                                                                [100%]

================================================== 1 passed in 0.01s ==================================================

...
[26] /app$ /app/.tox/py38/bin/pytest
================================================= test session starts =================================================
platform linux -- Python 3.8.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py38/.pytest_cache
rootdir: /app
collected 1 item                                                                                                      

test_module.py .                                                                                                [100%]

================================================== 1 passed in 0.01s ==================================================
_______________________________________________________ summary _______________________________________________________
  py36: commands succeeded
  py37: commands succeeded
  py38: commands succeeded
  congratulations :)
```

### Running tests with tox in Docker: advanced configuration

For a more complex use case, for instance, when you are working on a library that depends 
on some 3rd Python package, say, `pandas`, you can specify which versions of `pandas` 
you'd like to test your project's code with.
For the example below, your tests will be run in 6 different environments.

The `tox.ini` configuration file.

```    
[tox]
envlist = py36-pandas{112,113}, py37-pandas{112,113}, py38-pandas{112,113}
skipsdist = True

[testenv]
deps = 
  pandas112: pandas==1.1.2
  pandas113: pandas==1.1.3
  pytest
commands = pytest
```

The `test_pandas.py` containing a simple test function to create two data frames and compare them.

```python
import pandas as pd
from pandas._testing import assert_frame_equal

def test_pandas():
  df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
  df2 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
  assert_frame_equal(df1, df2)
```

The `pytest` output will be printed for each of the Python environments
in which the tests have been run (posted below with some sections removed for brevity).

```
[52] /app$ /app/.tox/py36-pandas112/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.6.9, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py36-pandas112/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.63s ====================================================================
[73] /app$ /app/.tox/py36-pandas113/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.6.9, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py36-pandas113/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.47s ====================================================================
[115] /app$ /app/.tox/py37-pandas112/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.7.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py37-pandas112/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.51s ====================================================================
[133] /app$ /app/.tox/py37-pandas113/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.7.5, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py37-pandas113/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.42s ====================================================================
[174] /app$ /app/.tox/py38-pandas112/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.8.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py38-pandas112/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.48s ====================================================================
[193] /app$ /app/.tox/py38-pandas113/bin/pytest
=================================================================== test session starts ===================================================================
platform linux -- Python 3.8.0, pytest-6.1.2, py-1.9.0, pluggy-0.13.1
cachedir: .tox/py38-pandas113/.pytest_cache
rootdir: /app
collected 2 items                                                                                                                                         

test_module.py .                                                                                                                                    [ 50%]
test_pandas.py .                                                                                                                                    [100%]

==================================================================== 2 passed in 0.38s ====================================================================
_________________________________________________________________________ summary _________________________________________________________________________
  py36-pandas112: commands succeeded
  py36-pandas113: commands succeeded
  py37-pandas112: commands succeeded
  py37-pandas113: commands succeeded
  py38-pandas112: commands succeeded
  py38-pandas113: commands succeeded
  congratulations :)
```

There are quite a few resources online that go deeper into how one can use `tox` in a Docker container,
but this simple layout has been very useful to me in various circumstances and may help others.

Happy testing!