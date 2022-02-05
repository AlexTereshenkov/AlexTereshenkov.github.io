title: Find and fix Python security issues with QL
date: 2019-09-09
modified: 2022-02-05
author: Alexey Tereshenkov
tags: python,QL
slug: find-fix-python-security-issues-with-ql
category: QL

[TOC]

> This is one of the few posts I wrote in 2019 when working for Semmle (later acquired by GitHub) that was originally published on the Semmle blog that was transformed. Python library for QL has changed quite a bit since then, however, many principles are still relevant and helpful for anyone who would want to learn more about QL. See [CodeQL for Python](https://codeql.github.com/docs/codeql-language-guides/codeql-for-python/) to learn more.

## Overview

In this blog post, we'll take a look at some security concerns
that are particularly relevant to Python developers.
There are already queries for some of these issues,
and we'll write new custom queries for the others.
You can execute any query in this post against your own Python project.

When you're writing code, it is very easy to accidentally introduce errors or vulnerabilities.
On top of that, you need to be aware of any existing bugs
in the implementation of the language you're working in,
which adds an additional burden.
For instance, CPython developers may need to review [security vulnerabilities](https://python-security.readthedocs.io/vulnerabilities.html)
present in the Python version they use.

Running static analysis on the source code can help you find
code that would produce an incorrect result,
open up hardware or software resources for malicious use,
or cause a program to unexpectedly fail.
Fixing those issues will make the program more secure.
To learn about the Python security model, bytecode safety,
and some typical security concerns, visit the [Python Security](https://python-security.readthedocs.io/security.html#python-security) resource
which has an excellent set of reference resources and further readings.

Unfortunately, for anyone who is maintaining a legacy Python 2 codebase,
and pre-2.7 versions in particular,
quite a few bugs and some security issues have been addressed only in Python 3.
So upgrading the code to the latest version of Python 3 is very often the only option
if you want to keep your code secure.
Although Python 3 is more secure than Python 2,
you still can't fully relax because it also suffers from security vulnerabilities,
even the most recent versions, such as Python 3.6, 3.7, and 3.8.
You can review the current security-related issues using the [Python bug tracker](https://bugs.python.org/).
On this website, you will find many bugs
which have a [CVE](https://cve.mitre.org/) number assigned such as CVE-2018-1000030 listed as [CVE-2018-1000030: Python 2.7 readahead feature of file objects is not thread safe](https://bugs.python.org/issue31530) or CVE-2013-4238 listed as [CVE-2013-4238: SSL module fails to handle NULL bytes inside subjectAltNames general names](https://bugs.python.org/issue18709) to mention just a few.

Here we categorize Python security concerns into two groups:

* Issues in the Python interpreter or standard library
written by Python core developers and contributors
* Issues in Python user code written by developers writing Python programs.

## Issues in CPython source code

If you are a developer writing your programs in Python,
you have very little control over the source code of CPython.
You could, of course, make the necessary changes to the source code
and compile your own Python interpreter,
however, this is something that only a few developers would find practical.

As an example, [the `urllib` module didn’t parse passwords containing the `#` character correctly](https://bugs.python.org/issue30500).
This bug was fixed in the most recent version of Python 3
and also backported to previous versions.
However, there are a few bugs that were fixed only in certain versions of Python
and were not backported.
For example, the [Hash function is not randomized properly](https://bugs.python.org/issue14621) bug
was fixed only in Python 3.4.0.
This means that previous versions, such as Python 3.3 and Python 2.7, are still vulnerable.
This puts some developers into a difficult situation
if they cannot upgrade to the latest Python interpreter to take advantage
of the latest security related fixes.

Semmle's continuous security analysis service, [LGTM.com](https://lgtm.com/),
includes the CPython project, analyzing both the C and Python source code.
If you develop security-sensitive applications,
you should review the security-related alerts that are highlighted in the latest code.
For example, the following alerts were found by queries that focus on potential vulnerabilities: [CPython's alert page](https://lgtm.com/projects/g/python/cpython/alerts/?mode=tree&tag=external%2Fcwe%2Fcwe-190%2Cexternal%2Fcwe%2Fcwe-192%2Cexternal%2Fcwe%2Fcwe-197%2Cexternal%2Fcwe%2Fcwe-377%2Cexternal%2Fcwe%2Fcwe-396%2Cexternal%2Fcwe%2Fcwe-546%2Cexternal%2Fcwe%2Fcwe-561%2Cexternal%2Fcwe%2Fcwe-563%2Cexternal%2Fcwe%2Fcwe-570%2Cexternal%2Fcwe%2Fcwe-571%2Cexternal%2Fcwe%2Fcwe-581%2Cexternal%2Fcwe%2Fcwe-628%2Cexternal%2Fcwe%2Fcwe-681%2Cexternal%2Fcwe%2Fcwe-685%2Cexternal%2Fcwe%2Fcwe-687%2Cexternal%2Fcwe%2Fcwe-825%2Csecurity) on LGTM.com.

## Issues in your own Python programs

In contrast, when you write your own Python programs,
often it's the choices that you make as you implement features
that determine the security of your program.
In the rest of this post, we look at some of the issues
that can make your programs less secure,
and provide guidelines on how avoid these common pitfalls.
We will also share built-in queries and custom queries
that you can use to find security-related issues in your code.

### Inadequate DSA and RSA key length

The paper [Transitioning the Use of Cryptographic Algorithms and Key Lengths](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf)
published by the [NIST Computer Security Resource Center](https://csrc.nist.gov/),
suggests using a key of size 2048 or larger for [RSA](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29)
and [DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm) algorithms.
The Python [cryptography](https://github.com/pyca/cryptography) package provides tools
for working with private keys and has a user `key_size` parameter.
See the Python code snippet in the [docs](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dsa/?highlight=generate_private_key#signing) for details.
From the [docs page](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dsa/?highlight=key_size):

> `key_size (int)` – The length of the modulus in bits.
> It should be either 1024, 2048 or 3072.
> For keys generated in 2015 this should be at least 2048.
> Note that some applications (such as SSH)
> have not yet gained support for larger key sizes specified in FIPS 186-3
> and are still restricted to only the 1024-bit keys specified in FIPS 186-2.

There is a built-in query, [Use of weak cryptographic key](https://lgtm.com/rules/1506737457159/),
that highlights when values smaller than 2048 are passed to the `key_size` parameter.

For example, the query would report an alert for this Python code:

```python
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.backends import default_backend
private_key = dsa.generate_private_key(
    key_size=512,
    backend=default_backend()
)
```

The query also identifies inadequate key lengths in code
that uses the `Crypto` and `Cryptodome` Python packages.
You can set a different minimum key length by [editing the query](https://lgtm.com/query/rule:1506737457159/lang:python/)
and changing the `result` of the `minimumSecureKeySize` predicate,
which is currently set to `2048` for both the DSA and RSA algorithms:

```ql
int minimumSecureKeySize(string algo) {
    algo = "DSA" and result = 2048
    or
    algo = "RSA" and result = 2048
    or
    algo = "ECC" and result = 224
}
```

### Using the deprecated 'pyCrypto' package

[PyCrypto](https://github.com/dlitz/pycrypto) is a mature Python cryptography toolkit
that has gained popularity over the years.
However, the package has quite a few issues, some of them affecting security,
and the project was last updated over five years ago.
One of those issues, [AES.new with invalid parameter crashes python](https://github.com/dlitz/pycrypto/issues/176),
is actually an exploitable vulnerability, [CVE-2013-7459](https://security-tracker.debian.org/tracker/CVE-2013-7459).

The current recommendation is to use some other Python package.
For instance, `cryptography`, is a popular choice for many Python developers:
* [`paramiko`](https://github.com/paramiko/paramiko), one of the popular native Python SSHv2 protocol libraries,
has switched to `cryptography` from `pyCrypto`;
see [this pull request](https://github.com/paramiko/paramiko/pull/394) for details.

* [`twisted`](https://twistedmatrix.com/trac/), a popular event-driven networking engine,
has switched to `cryptography` from `pyCrypto` as well;
see [this pull request](https://twistedmatrix.com/trac/ticket/7413) for details.

To check if there are any places where the `pyCrypto` package is imported
and used, as in this Python code snippet:

```python
from Crypto.Hash import SHA256
val = SHA256.new('abc'.encode('utf-8')).hexdigest()
```

we could write the following custom query:

```ql
/**
 * @name Using a deprecated pyCrypto package
 * @description Using an unmaintained tool kit with multiple security
   issues makes your code vulnerable to attack.
 * @kind problem
 * @tags security
 * @problem.severity error
 * @id py/using-insecure-pycrypto-package
 */

import python

from ImportExpr imp, Stmt s, Expr e, string moduleName
where
  moduleName = imp.getName() and
  s.getASubExpression() = e and
  (e = imp or e.contains(imp)) and
  (moduleName.matches("Crypto") or moduleName.matches("Crypto.%"))
select imp, "pyCrypto package has multiple security issues"
```

If your project is on LGTM.com, you can set up [automated code review](https://lgtm.com/help/lgtm/managing-automated-code-review)
and [add this query to your repository](https://lgtm.com/help/lgtm/writing-custom-queries) to ensure
that you never accidentally introduce uses of the `pyCrypto` package.

### Binding to all IP addresses with the 'socket' module

When you're using the built-in `socket` module (for instance, to build a message sender service),
it's possible to bind to all available IPv4 addresses by specifying `0.0.0.0` as the IP address.
When you do this, you essentially allow the service to accept connections from any IPv4 address
provided that it is capable of reaching it through routing.
Note that an empty string `''` has the same effect as `0.0.0.0`.
Opening up your end point to all network interfaces is considered to be insecure.

For example:

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 6080))
s.bind(('192.168.0.1', 4040))
s.bind(('', 8888))
```
From the Python [socket documentation](https://docs.python.org/3/library/socket.html#socket-families):

> A pair `(host, port)` is used for the `AF_INET` address family,
> where *host* is a string representing either a hostname
> in Internet domain notation like 'daring.cwi.nl' or an IPv4 address like '100.50.200.5',
> and *port* is an integer.

The following custom query would find these insecure bindings:

```ql
/**
 * @name Binding a socket to all network interfaces
 * @description Binding a socket to all interfaces would
   open up traffic from any IPv4 address
 * and is therefore associated with security risks.
 * @kind problem
 * @tags security
 * @problem.severity error
 * @id py/bind-socket-all-network-interfaces
 */

import python

Value aSocket() { result.getClass() = Value::named("socket.socket") }

CallNode socketBindCall() {
  result = aSocket().attr("bind").(CallableValue).getACall()
}

string allInterfaces() { result = "0.0.0.0" or result = "" }

from CallNode call, string address
where
  call = socketBindCall() and
  address = call.getArg(0).getNode().(Tuple).getElt(0).(StrConst).getText() and
  address = allInterfaces()
select call.getNode(), "'" + address + "' binds a socket to all interfaces."
```

### Using insecure SSL versions

There have been quite a few security changes in Python 3's built-in `ssl` module.
This is particularly true for versions 3.6 and 3.7.
Visit [Python SSL and TLS security](https://python-security.readthedocs.io/ssl.html)
to learn about evolution of the `ssl` module.
SSL versions 2 are 3 are now considered to be insecure
and official Python documentation discourages their use.
Since Python 3.6, many protocol versions
such as `ssl.PROTOCOL_SSLv23` and `ssl.PROTOCOL_SSLv2`, are deprecated
and OpenSSL has removed support for `SSLv2`.

From Python 3.6 onward, it is best to use the `ssl.PROTOCOL_TLS` protocol.
From the [docs page](https://docs.python.org/3/library/ssl.html#ssl.PROTOCOL_TLS):

> `ssl.PROTOCOL_TLS`: Selects the highest protocol version that both the client and server support.

Although you can specify the SSL version in an `ssl.wrap_socket` call,
this was deprecated in version 3.7.
Instead, the use of a more secure alternative is suggested by the [Python docs](https://docs.python.org/3/library/ssl.html#ssl.wrap_socket):

> Since Python 3.2 and 2.7.9,
> it is recommended to use the `SSLContext.wrap_socket()` instead of `wrap_socket()`.
> The top-level function is limited
> and creates an insecure client socket without server name indication or hostname matching.

There is a built-in query, [Default version of SSL/TLS may be insecure](https://lgtm.com/rules/1507225275976/),
which finds uses of `SSLContext.wrap_socket()`.
For earlier versions of Python, you want to make sure
that you're not using insecure versions of SSL
such as `ssl.PROTOCOL_SSLv2` or `ssl.PROTOCOL_SSLv3`.
For this, there is another built-in query, [Use of insecure SSL/TLS version](https://lgtm.com/rules/1507248366243/),
which finds insecure SSL/TLS versions both for `pyOpenSSL.SSL`
(a Python wrapper around the `OpenSSL` library)
and for the built-in `ssl` module.

### Not validating certificates in HTTPS connections

During an HTTPS request, it is important to verify SSL certificates,
which is exactly what any modern web browser does nowadays.
Up to versions Python 2.7.9 (for Python 2) and Python 3.4.3 (for Python 3),
CPython modules that dealt with HTTP interaction (such as `httplib` and `urllib`)
did not verify the web site certificate against a trust store.
This issue was registered as [CVE-2014-9365](https://nvd.nist.gov/vuln/detail/CVE-2014-9365)
and is an example of [CWE-295: Improper Certificate Validation](http://cwe.mitre.org/data/definitions/295.html)
which can potentially lead to a [man-in-the-middle (MITM) attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

A de-facto standard library used by the Python community for communicating over HTTP is `requests`.
By default, it has [SSL verification enabled](https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification),
and a custom exception will be thrown if certificate verification fails.
However, it is possible to disable the verification that TLS provides:

```python
import requests
requests.get('https://example.com', verify=False)
```

To find HTTP requests that fail to verify the certificate, you can run the built-in query, [Request without certificate validation](https://lgtm.com/rules/1506755127042/).

### Compromising privacy in universally unique identifiers

[Universally unique identifiers (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier)
can be generated using the [`uuid`](https://docs.python.org/3.6/library/uuid.html) module.
The general recommendation is to use `uuid1()` or `uuid4()` to generate a unique identifier.
However, `uuid1()` may compromise privacy
because the UUID will include the computer’s network address.

`uuid4()`, in contrast, creates a random UUID
and is simply a convenience function.
From the [CPython source code](https://github.com/python/cpython/blob/master/Lib/uuid.py#L778):

```python
def uuid4():
    """Generate a random UUID."""
    return UUID(bytes=os.urandom(16), version=4)
```

Furthermore, there are some concerns about the "safety" of UUIDs.
From the [Python docs](https://docs.python.org/3.7/library/uuid.html):

> Depending on support from the underlying platform,
> `uuid1()` may or may not return a "safe" UUID.
> A safe UUID is one which is generated using synchronization methods
> that ensure no two processes can obtain the same UUID.

To find version 1 UUIDs generated by `uuid.UUID(bytes=values, version=1)`
or `uuid.uuid1()`, as in the code snippet below,

```python
import os
import uuid

id1 = uuid.uuid1()
id2 = uuid.UUID(bytes=os.urandom(16), version=1)
id3 = uuid.UUID(None, b'1234567891234567', None, None, None, 1)
```

we can run the following custom query:

```ql
/**
 * @name Using a uuid1 for generating UUID
 * @description uuid1 will use machine's network address
   for generating UUID and may compromise privacy.
 * @kind problem
 * @tags security
 * @problem.severity error
 * @id py/using-uuid1-for-UUID
 */

import python

from CallNode call
where
  call = Value::named("uuid.uuid1").getACall()
  or
  call = Value::named("uuid.UUID").getACall() and
  (
    call.getArgByName("version").getNode().(IntegerLiteral).getValue() = 1 or
    call.getArg(5).getNode().(IntegerLiteral).getValue() = 1
  )
select call, "uuid1 will use machine's network address and may compromise privacy."
```

### Use of 'assert' statements to control program flow

The `assert` statement can be used in Python to indicate
when executing the code would result in program failure
or the retrieval of incorrect results.
It is very common to use `assert` in unit and integration tests.
However, `assert` statements are disabled
when [you run a Python program with optimization enabled](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE).
Running `python -O program.py` means that `assert` statements are ignored
which may give a certain performance boost
(either significant or negligible
depending on how time-consuming the `assert` statements are).

This means that it can be unwise to rely on `assert` statements
to define the logic of a program execution flow,
if you plan to run your Python programs with optimization enabled
or the code may be run outside of your control.
Moreover, use of `assert` statements can be associated with security risks.
Consider this Python code snippet:

```python
def get_customers(user):
    """Get list of customers."""
    assert is_superuser(user), "User is not a member of superuser group"
    return db.lookup('customers')
```

When this program is run in optimized mode,
the `assert` statement will be ignored
and any user would be able to get a list of customers,
regardless of whether they are a member of the `superuser` group or not.

This code can be rewritten more securely, without `assert` statements, as:

```python
def get_customers(user):
    """Get list of customers."""
    if not is_superuser(user):
        raise PermissionError("User is not a member of superuser group")
    return db.lookup('customers')
```  

Writing a custom query that catches all `assert` statements is trivial,
however, all legitimate uses of `assert` would also be caught
so you would need to look through each result manually.
Optionally, you could search for `assert` statements used outside of tests.
This query searches for all `is_superuser` function calls within the `assert` statements.

```ql
import python

from AstNode ast, Assert assert
where
  assert.contains(ast) and
  ast.(Call).getFunc().(Name).getId() = "is_superuser"
select ast
```  

### Parsing external files content into Python objects

Python provides multiple ways to read external files
and load their content into Python objects.
There are `exec` and `eval` built-in functions
along with `pickle` (or `cPickle` in Python 2).
External packages such as [`PyYAML`](https://pyyaml.org/wiki/PyYAMLDocumentation)
can also be used to parse YAML file contents.

Because data from external sources may not be secure,
the general security guidelines are that you should never unpickle
or load by parsing any data received from an untrusted source.

There is a built-in query, [Deserializing untrusted input](https://lgtm.com/rules/1506218107765/),
that highlights code that may be a security concern
when unpickling and other deserialization happens.
The general recommendation is to avoid constructing arbitrary Python objects via `pickle`
or via a `pyYAML` package if the data comes from an untrusted source (the internet in particular).
`PyYAML`, however, has the `safe_load` function
which limits what can be loaded to simple Python objects.

In this Python code snippet, a class instance is created based on the YAML file contents
(posted here as a string in `yaml.load` for brevity):

```python
import yaml

class PasswordReader(object):

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as fh:
            return fh.readlines()

    def __repr__(self):
        return f"PasswordReader: {self.path}"


obj = yaml.load("""
!!python/object:__main__.PasswordReader
path: /etc/passwd
""")
print(obj)
```

Using `yaml.safe_load` would block construction of the class instance object
unless it has been marked as safe.
To be considered safe, it should inherit from `yaml.YAMLObject`
and have a property `yaml_loader` set to `yaml.SafeLoader`.

This custom query was written to find unsafe `yaml.load` calls in your codebase:

```ql
/**
 * @name Using insecure yaml.load function
 * @description yaml.load function may be unsafe
   when loading data from untrusted sources
 * @kind problem
 * @tags security
 * @problem.severity error
 * @id py/using-yaml-load
 */

import python

from CallNode call
where call = Value::named("yaml.load").getACall()
select call.getNode(), "yaml.load function may be unsafe when
loading data from untrusted sources. Use yaml.safe_load instead."
```

This type of custom query, where you search for a specific function call, is fairly common.
This approach can be used for any language feature that was considered safe a few years ago
but the current recommendation is to use a newer version or an alternative, more robust one.

For examples of how you can write your own queries to find the use of a certain function
or import of a module, review the following built-in queries:

* [Deprecated slice method](https://lgtm.com/rules/9980084/)
* [Import of deprecated module](https://lgtm.com/rules/4860084/)
* [Use of exit() or quit()](https://lgtm.com/rules/3960095/)

In most cases, you want to make sure
that the older or less secure function could not be used in the new code being written.
The power of writing your own custom queries, however, lies in
the ability to go beyond built-in queries
and to look for the functions or class methods that you decide to blacklist.
You can write a new query to trigger an alert
if a blacklisted function is found.
[LGTM.com](https://lgtm.com/) provides [automatic code review functionality]([https://lgtm.com/help/lgtm/managing-automated-code-review])
to prevent bugs from ever making it to your project.
If you add custom queries to your repository, then you'll also get alerts if a pull request contains functions or class methods that you've blacklisted.  

### References

Here are some references to Python security resources you may find useful.

* [National Vulnerability Database](https://nvd.nist.gov/)
* [MITRE CWE database](https://cwe.mitre.org/)
* [Python bug tracker](https://bugs.python.org)
* [Python vulnerability statistics](https://www.cvedetails.com/vendor/10210/Python.html)
* [OpenStack Secure Development Guidelines](https://security.openstack.org/#secure-development-guidelines)
* [Security related built-in Python queries](https://help.semmle.com/wiki/label/python/security)
* [Bandit - Python security tool](https://bandit.readthedocs.io/en/latest/)
* [Python security overview](https://python-security.readthedocs.io/security.html)
* [Python security vulnerabilities](https://python-security.readthedocs.io/vulnerabilities.html)
