title: Using python3-apt Debian package for system package management with Python
date: 2020-12-01
modified: 2020-12-01
author: Alexey Tereshenkov
tags: python,docker,testing,linux,apt,debian
slug: use-apt-from-python
category: python

[TOC]

For Debian-based systems such as Ubuntu, most package management happens via the `apt`
system package.
It provides a friendly command line interface, however, there aren't many robust ways to use
it in some other way other than via a terminal.
Fortunately, there is a Python package, `python3-apt`, which provides a Python 3 interface 
to the `libapt-pkg` library.
With this package, you'll be able to list installed packages, check what packages are 
available for installation, install new packages and so much more.

## Installation

`python3-apt` package should be installed with `apt`.
The sources are currently available at 
[GitLab: python-apt repo](https://salsa.debian.org/apt-team/python-apt).
There isn't a great amount of resources that will help you get started with `python3-apt`,
but the [official documentation](https://apt-team.pages.debian.net/python-apt/library/index.html) 
is very comprehensive.

To experiment with the basic usage of the `python3-apt` package, let's define a Docker image:

    :::docker
    FROM ubuntu:18.04

    RUN apt-get -qq update
    RUN apt-get install -y --no-install-recommends \
        python3-apt \
        ca-certificates \        
        gnupg

and build it:

    :::bash

    $ docker build -t python-apt-docker .

## Installing a package

Let's install a package, make sure that it's available, and then delete it.
This can be useful when you need to install a package, but simply using `subprocess`
to make a system command call won't suffice.
Parsing `apt` output is very unreliable and is strongly discouraged.

{% include_code pythonapt/install_tree.py lang:python :hideall: %}

Let's run this code in a Docker container:

    :::bash
    $ docker run -it --rm -v ${PWD}/:/project python-apt-docker /bin/bash -c 'python3 /project/install_tree.py'
    tree executable location: None
    debconf: delaying package configuration, since apt-utils is not installed
    Selecting previously unselected package tree.
    (Reading database ... 5200 files and directories currently installed.)
    Preparing to unpack .../tree_1.7.0-5_amd64.deb ...
    Unpacking tree (1.7.0-5) ...
    Setting up tree (1.7.0-5) ...
    Package installed: True; version: 1.7.0-5
    Package location: /usr/bin/tree
    (Reading database ... 5207 files and directories currently installed.)
    Removing tree (1.7.0-5) ...
    tree executable location: None

## Checking what packages are installed

Let's find out what Python related packages are available in a system.
This can be handy for a script that makes sure that system dependencies have
been installed.

{% include_code pythonapt/list_pythons.py lang:python :hideall: %}

Let's run this code in a Docker container:

    :::bash
    $ docker run -it --rm -v ${PWD}/:/project python-apt-docker /bin/bash -c 'python3 /project/list_pythons.py'
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    python3.6
    python-apt-common
    python3
    python3.6-minimal
    python3-minimal
    python3-apt

## Adding additional Debian sources

If the default sources available for system packages do not provide the packages you need
(which is a common case for legacy packages or corporate environment Debian pools),
it is possible to add additional `apt` sources using [SourcesList](https://wiki.debian.org/SourcesList)
on demand.

### Adding public sources

{% include_code pythonapt/install_from_public.py lang:python :hideall: %}

Let's run this code in a Docker container:

    :::bash
    $ docker run -it --rm -v ${PWD}/:/project python-apt-docker /bin/bash -c 'python3 /project/install_from_public.py'
    {'', 'http://archive.ubuntu.com/ubuntu/', 'http://archive.canonical.com/ubuntu', 'http://security.ubuntu.com/ubuntu/'}
    {'', 'http://archive.ubuntu.com/ubuntu/', 'http://archive.canonical.com/ubuntu', 'http://security.ubuntu.com/ubuntu/', 'http://download.virtualbox.org/virtualbox/debian'}
    # deb http://archive.canonical.com/ubuntu bionic partner
    # deb-src http://archive.canonical.com/ubuntu bionic partner

    deb http://security.ubuntu.com/ubuntu/ bionic-security main restricted
    # deb-src http://security.ubuntu.com/ubuntu/ bionic-security main restricted
    deb http://security.ubuntu.com/ubuntu/ bionic-security universe
    # deb-src http://security.ubuntu.com/ubuntu/ bionic-security universe
    deb http://security.ubuntu.com/ubuntu/ bionic-security multiverse
    # deb-src http://security.ubuntu.com/ubuntu/ bionic-security multiverse
    deb [trusted=yes] http://download.virtualbox.org/virtualbox/debian bionic contrib

### Adding private sources

To add private sources (that may require authentication), you would need to make some changes.
In the Docker image, you may need to download the GPG key from the server that hosts Debian packages.
The key can be added later using the `apt-key add` command.

You would also need to add authentication file(s) to the `/etc/apt/` directory so that `apt`
would be able to use the authentication details when attempting to download the Debian packages
from the private repository.
[`apt_auth.conf`](https://manpages.debian.org/testing/apt/apt_auth.conf.5.en.html) files 
can be handled using a built-in `netrc` Python module so writing a custom file parser is not necessary.

Once the `sources.list` has the private repository listed, you can install the packages from
the repository that requires authentication in the same way as we have installed the `tree` package earlier.

Happy packaging!