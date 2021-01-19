title: Patching with unittest.mock for Python testing: cheat sheet
date: 2020-11-20
modified: 2021-01-19
author: Alexey Tereshenkov
tags: python,mock,testing,patch
slug: patching-mock-python-unit-testing
category: python

[TOC]

### Overview of patching

Python built-in `unittest` framework provides the 
[`mock`](https://docs.python.org/3/library/unittest.mock.html) module 
which gets very handy when writing unit tests.
It also provides the [`patch`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch)
entity which can be used as a function decorator, class decorator or a context manager.

The basic idea behind patching is that it lets you temporarily change the object that is being used when your test runs.
For example, if you are testing a function that needs to read some data out
of a database, you can patch it so that you don't need to 
communicate with any external services when unit tests run.

Given this piece of code, we are interested in testing the `get_customers()` function.
We have tests in place for functions (`validate_input` and `fetch`) that this function calls,
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

In the rest of the post, we will explore typical use cases for patching and mocking.

## Patching class initialization

Use case: 

You want to test a class method, but initializing a class instance would
require a lot of additional mocking to pass valid input parameters. 
You also want to avoid any real initialization operations, but would still
want to have some of the class instance variables set.

Code:

    :::python
    class FileProcessor:
        def __init__(self, files: List[Path], process_config: ProcessorConfiguration):
            self.files = files
            self.process_config = process_config
        
        def validate_files(self):
            # operate on the files and return some validation result
            ...

Test:

    :::python
    def test_validate_files():
        with patch.object(FileProcessor, '__init__', lambda self: None):
            fp = FileProcessor()
            fp.files = [Path('foo'), Path('bar')]
            assert fp.validate_files().get("status") == ValidationStatus.SUCCESS

            fp.files = []
            assert fp.validate_files().get("status") == ValidationStatus.FAILURE

## Patching static, class, and instance methods

Use case:

You have a class for which you want to patch some of the class instance methods,
class methods, or static methods.
You would need to patch a method of interest and the process of patching the methods 
is universal for all the methods types.

Code:

    :::python
    class Address:

        def __init__(self, house: str, street: str, postal_code: str, city: str):
            self.house = Address.numerize(house)
            self.street = street
            self.postal_code = postal_code
            self.city = city

        @classmethod
        def from_tuple(cls, *address_tuple: Tuple):
            return Address(*address_tuple)

        @staticmethod
        def numerize(value):
            return int(value)

        def to_string(self):
            return f"{self.house}{self.street}\n{self.postal_code}\n{self.city}"

        def print(self):
            fmt = self.to_string()
            print(fmt)
            return fmt

    def is_valid_address(address_tuple):
        try:
            Address.from_tuple(*address_tuple)
            return True
        except Exception:
            return False

Test:

    :::python
    def test_is_valid_address():
        with patch('static_class.Address.from_tuple', lambda *data: True):
            assert is_valid_address(("1", "New Road", "99999", "City"))
        
        with patch('static_class.Address.from_tuple', side_effect=Exception()):
            assert not is_valid_address(("1", "New Road", "99999", "City"))

    def test_address_construct():
        with patch('static_class.Address.numerize', lambda value: 9999):
            address = Address(*("1", "New Road", "99999", "City"))
            assert address.city == "City"
            assert address.house == 9999

    def test_print():
        with patch('static_class.Address.to_string', lambda value: "Address formatted"):
            address = Address(*("1", "New Road", "99999", "City"))
            assert address.print() == "Address formatted"

## Patching a nested class instance attribute

Use case:

You have a class that when instantiated has an attribute that itself is
an instance of a class with additional instance attributes.
You are interested in patching this nested attribute to be set to some
value.

Code:

    :::python
    from typing import List


    class City:
        def __init__(self, name: str):
            self.name = name


    class Address:
        def __init__(self, address: List[str]):
            self.city = City(address[0])
            self.street = address[1]
            self.house = address[2]


    class Customer:
        def __init__(self, address: List[str]):
            self.address = Address(str)

        def get_address(self):
            return self.address

Test:

We want to patch the `get_address()` method on the class instance 
and then set a returned object to have a nested attribute set to some value.
This may be necessary when you are trying to cover a code branch which
will be executed only when a value of the nested attribute is equal to a certain value.

    :::python
    from typing import List
    from unittest.mock import patch, MagicMock

    def test_customer_address():
        with patch('customer.Customer') as mock_customer:
            c = mock_customer.return_value
            mock_address = MagicMock()
            # MagicMock lets you define nested attributes
            mock_address.city.name = "BigCity"
            c.get_address.return_value = mock_address
            assert c.get_address().city.name == 'BigCity'


## Patching class instance method that modifies `self`

Use case:

You have a method which doesn't return anything but instead sets 
or modifies its object (`self`) properties.
You cannot patch the mock's method with `.return_value` 
and thus need instead modify the values of the `self`.

Code:

    :::python
    class Client:

        def __init__(self, guid):
            self.guid = guid
            self.visited = False
            self.last_time_visited = None

        def visit(self):
            self.visited = True
            self.last_time_visited = datetime.now()

        def process(self):
            self.visit()

Test:

We would like to test the `process()` method without letting it to execute the `visit()` method,
but still check that after running the `process()` method, the `Client` instance would get
certain fields set.

    :::python
    from client import Client

    def setattrs(obj, **kwargs):
        for k, v in kwargs.items():
            setattr(obj, k, v)


    def test_process():
        mock_client = Mock()
        with patch('client.Client', lambda: mock_client):
            mock_client.process.side_effect = lambda: setattrs(mock_client,
                visited=True, last_time_visited=datetime.now())
            client = Client(99)
            client.process()
            assert client.visited is True
            assert isinstance(client.last_time_visited, datetime)

## Patching multiple calls to the same function 

Use case: 

You call a function being mocked multiple times in the source code being tested 
and need to return a different value for each call.
For instance, you mock a function call that will check whether 
a database table exists, then you call a function to delete it, 
and then use the first function again to make sure 
that the table does not exist (i.e., it was successfully deleted).

You cannot simply mock the function with the `patch` because it will
then return the same value.
You have to use the `Mock().side_effect` property.
The `side_effect` collection can even have an exception initialization
if at a certain time you call the mocked function a particular exception is
expected to be raised: `side_effect = [10, 15, ValueError()]`.

Code:

    :::python
    def get_table(name):
        return True

    def delete_table(name):
        return True


    def delete_db_table(table_name: str) -> bool:
        if get_table(table_name):
            delete_table(table_name)
            if not get_table(table_name):
                return True
            else:
                raise ValueError(f"Failed to delete table {table_name}")
        return True

Test:

    :::python
    @patch('db.delete_table', lambda name: True)
    def test_delete_db_table():    
        get_table_mock = Mock()
        
        # db table gets deleted
        get_table_mock.side_effect = [True, False]
        with patch('db.get_table', get_table_mock):
            assert delete_db_table("LogHistory")

        # db table fails to be deleted
        get_table_mock.side_effect = [True, True]
        with patch('db.get_table', get_table_mock):
            with pytest.raises(ValueError):
                delete_db_table("LogHistory")

## Patching function and its returned object

Use case:

When you patch a function or a method, it may be the case that the object
that it will return may have own methods that you would want to patch.
For instance, when patching `subprocess.run()` that returns a `CompletedProcess` object,
you may want to patch its `.check_returncode()` method to return some value.
Just as with the `Mock().side_effect()`, it's possible to create side effects for methods
of a `Mock()` object.

Code:

    :::python
    def call_cmd(cmd: str):
        res = subprocess.run(cmd)
        return res.check_returncode()

Test:

    :::python
    def test_call_cmd():
        run_mock = Mock()
        run_mock.check_returncode.return_value = "0"
        with patch('subprocess_run.subprocess.run', lambda cmd: run_mock):
            assert call_cmd('du -sh lib') == "0"
        
        run_mock = Mock()
        run_mock.check_returncode.side_effect = subprocess.CalledProcessError(0, 0)
        with patch('subprocess_run.subprocess.run', lambda cmd: run_mock):        
            with pytest.raises(CalledProcessError):
                call_cmd('du -sh non-existing-dir')

## Patching class properties

Use case:

You have a class with one or more properties decorated with the `@property`.
Mocking them requires special handling using the `unittest.mock.PropertyMock` object.
This is useful when the initialization of an object's property is complex
and is not really required for a particular unit test.

Code:

    :::python
    class Process:
        def __init__(self, pid: int):
            self._pid = pid
            
        @property
        def pid(self):
            return self._pid

        def as_string(self):
            return f'Process({self.pid})'

Test:

    :::python
    def test_process_pid_property():
        with patch.object(Process, '__init__', lambda self: None):
            with patch('class_properties.Process.pid', new_callable=PropertyMock) as mock_pid:
                mock_pid.return_value = 99
                process = Process()
                assert process.as_string() == 'Process(99)'

## Patching opening a file with `open`

Use case:

You have a function that is interacting with the file system by opening a file.
A helper function `unittest.mock.mock_open` can be used to replace the use of `open`.

Code:

    :::python
    def read(path):
        with open(path) as f:
            return f.readlines()


Test:

    :::python
    def test_read_file():
        with patch('read_file.open', mock_open(read_data="lines")):
            assert read('dir/path') == ["lines"]
    

## Notes

1. When mocking is required for too many places, it may be the case that your class or a function
is too big and would be a good candidate for refactoring.
To make mocking for a large (or complex) code unit easier, you can use 
[`unittest.mock.MagicMock()`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock)
instead.

2. When patching code that is interacting with the file system too often,
patching all the `os`, `pathlib`, and `shutil` things can get tedious rather quickly.
You may want to take a look at the virtual file system, [pyfakefs](http://jmcgeheeiv.github.io/pyfakefs/release/), to be used when testing.
Keep in mind that you won't be able to use `mock.patch` to patch your file system 
interaction functions when you use `pyfakefs` because it patches them on its own.

3. When your programs are really scripts that process some files, you may be better off
writing good integration tests using real data instead.
This could be particularly true when your Python program is relying on using non-Python 
code such as compiled C (for which you have no source code) to read/process/write data.
In this situation, you won't be able to use the `pyfakefs` virtual file system and mocking
all the interaction between your Python programs and external tools can be tedious.

4. If the programs for which you write unit tests interact with external web services 
over HTTP a lot, you may look into the [`vcrpy`](https://github.com/kevin1024/vcrpy) 
package that can automatically mock your HTTP interactions.
The [`pytest-recording`](https://github.com/kiwicom/pytest-recording) 
plugin provides handy custom markers.

Happy patching!                