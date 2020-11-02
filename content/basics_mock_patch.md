title: Patching with unittest.mock for Python testing: cheat sheet
date: 2020-09-30
modified: 2020-09-30
author: Alexey Tereshenkov
tags: python,mock,testing,patch
slug: patching-mock-python-unit-testing
category: python
status: draft

[TOC]

### Overview of patching

Python built-in `unittest` framework provides the `mock` module which gets very handy
when writing unit tests.
It also provides the [`patch`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch)
entity which can be used as a function decorator, class decorator or a context manager.

The basic idea behind patching is that it lets you temporarily change the object that is being used when your test is run.
If you are testing a function that needs to read some data out
of a database, you can patch it so that you don't need to 
communicate with any external services when unit tests are run.

Given this piece of code, we are interested in testing the `get_customers()` function.
We have tests in place for functions (`validate_input` and `fetch`) that this functions calls,
so that we can ignore them.

    :::python
    def get_customers(city: str):
        validate_input(object_type=CITY, value=city)
        customers = fetch(query=f'customers;city={city}')
        return customers

To patch those functions, instead of calling them at the execution time, 
anonymous lambda functions could be used.
For the `validate_input()` function, we are not interested in the return value; however, for the
`fetch` function we are.
 
    :::python
    from unittest.mock import patch
    from utils import get_customers

    @patch('utils.validate_input', lambda object_type, value: None)
    def test_get_customers():
        expected_customers = ['Customer1', 'Customer2']
        with patch('utils.fetch', lambda query: expected_customers):
            actual_customers = get_customers(city='Paris')
            assert actual_customers == expected_customers

The patched `fetch` function doesn't have to return any meaningful value as we will only be testing
whether it returned what the patching function is supposed to return.
However, I often find it to be easier to understand the context and business logic when
some more real values are used.
Note that the `patch()` was used both as a context manager and as a test function decorator.

In the rest of the post, we will explore typical use cases for patching.

TBC
