title: Using Docker for Python development: cheat sheet
date: 2020-09-07
modified: 2020-09-07
author: Alexey Tereshenkov
tags: python,docker,testing
slug: docker-for-python-cheat-sheet
category: python

[TOC]

The Docker framework can be an extremely useful tool for any Python developer
who wants to run their Python programs (either for development or testing purposes) 
in a certain isolated environment with a pre-defined set of system and Python packages
installed.
Docker can also help with testing your Python code against multiple versions of the
Python packages in multiple operating systems.

The beauty of Docker is that you don't need to understand the intricate details of how
Docker technology works to take advantage of it.
This blog post contains recipes any Python developer can benefit from regardless how
experienced you are with Docker and containerization techniques.

Each recipe or scenario is based on a problem that one may need to solve and provides
a solution in form of a `Dockerfile` file, a `docker build`, and a `docker run` command.

### Basic setup

The base Docker image you'll be using will likely to be different depending on a number
of factors, however, to keep the build time short, I'll be using the `alpine` image in 
most cases.

Dockerfile contents:

    :::docker

    FROM python:3.7-alpine
    CMD ["python3", "--version"]

The build step contains the `-t` flag which defines the tag name of the image 
that will be built.
The dot (`.` ) tells Docker to use the the file named `Dockerfile` in the current directory.

Building a Docker image:

    :::bash

    $ docker build -t snake .

When an image is run, the `CMD` command found in the Dockerfile is executed.
The `--rm` (remove) flag will make sure to delete the container once the `run`
command is complete.

Running a Docker image:

    :::bash

    $ docker run --rm snake
    # Python 3.7.9

### Experiment with a Python REPL of any version

    :::docker

    FROM python:3.7.8-alpine
    CMD ["python3"]

By changing the version, you can get into an interactive Python console
for the given version.
This is very handy when you want to test how a certain feature works
in a newer or an older Python version.

When a `docker run` command is executed, it will run the `CMD` command and exit,
so you won't be able to interact with the REPL.
To work with the container in an interactive mode, the `-it` flag should be used.

    :::bash

    $ docker run --rm -it snake
    # Python REPL becomes available

### Passing a command to a Python Docker image

    :::docker

    FROM python:3.7.8-alpine

When running a Docker container, it's possible to pass a command, optionally,
with additional arguments.
Python provides support for running a command with 
the [`-c` option](https://docs.python.org/3/using/cmdline.html#cmdoption-c)
so that it's possible to supply the program code as a string.
This can be very handy when you need to have a one-liner for an operation that
will return a value you may need later as input for the subsequent operations.

    :::bash

    $ docker run --rm -it snake python3 --version
    # Python 3.7.8

    $ docker run --rm -it snake python3 -c "import sys; print(sys.platform)"
    # linux

### Run a Python program from the host in a Docker container

    :::docker

    FROM python:3.7.8-alpine

It is possible to mount a local directory (on your disk) as a volume to a Docker 
container which is done with the `-v` parameter.

Running the command below will make the `app` directory files available in the
Docker container.
This approach can be used when you want to run a Python program in a Docker
container likely having a different system environment and Python version installed.

Having this Python program (stored at `app/main.py`):

    :::python
    import sys
    print(sys.version_info)

you can execute it with:

    :::bash
    $ docker run -v ${PWD}/app:/app snake python3 /app/main.py
    # sys.version_info(major=3, minor=7, micro=8, releaselevel='final', serial=0)

It is also possible to copy files to the Docker image when the image is being built
if you don't want to mount any volumes at the run time.

    :::docker

    FROM python:3.7.8-alpine
    WORKDIR /opt/project/app
    COPY ./app
    CMD ["python3", "main.py"]

You can now run the Docker container to execute the `main.py` file that was copied:

    :::bash
    $ docker run --rm snake
    # sys.version_info(major=3, minor=7, micro=8, releaselevel='final', serial=0)

Alternatively, you could also make the `CMD` command a part of the `docker run`:

    :::docker

    FROM python:3.7.8-alpine
    WORKDIR /opt/project/app
    COPY ./app

Then you pass the arguments to the container from the shell instead:

    :::bash
    $ docker run --rm snake python3 main.py
    # sys.version_info(major=3, minor=7, micro=8, releaselevel='final', serial=0)

### Get into a Docker container shell and run a command

    :::docker
    
    FROM python:3.7.8-alpine
    WORKDIR /opt/project/app
    COPY ./app .

It is possible to start a Docker container and run a shell console to execute arbitrary
commands.
This resembles connecting to a remote machine via an SSH connection or using a local Bash console.

    :::bash
    $ docker run --rm -it snake /bin/sh           
    # /opt/project/app # ls
    # main.py
    # /opt/project/app # python3 main.py
    # sys.version_info(major=3, minor=7, micro=8, releaselevel='final', serial=0)

### Access files created in the Docker container on the host

Accessing files that are created by processes run in a Docker container is possible
by mounting a volume.

    :::docker

    FROM python:3.7.8-alpine
    WORKDIR /opt/project/app

Now you can run the container in the interactive mode and attach a shell console:

    :::bash
    $ docker run -it -v ${PWD}/app:/opt/project/app snake /bin/sh 
    # > touch foo.bar

The `foo.bar` file will appear on your host disk under the `app` directory.
This makes it possible to create arbitrary files within your Docker container
saving them on your host disk making them accessible for further usage locally.

### Copy files produced by Docker build command to the host

In certain cases, a Dockerfile may create new files which can be accessed
when starting the container.

    :::docker
    FROM alpine
    RUN echo "some data" > /home/data.out

The trick here is to mount your host's directory to some other directory than container's `home`
and then copy the file(s) you need to this intermediate location.

    :::bash
    $ docker run --rm -it -v ${PWD}/datadir:/home/datadir snake
    # cp /home/data.out /home/datadir/

At this point, the `data.out` file should appear on your host's disk 
under the `datadir` directory in your current working directory.

### Run Python tests stored on your host inside a Docker container

To do this, one would need to have a Docker container with the `pip` installed and
the necessary Python packages that are required by your tests.
It can be wise to install a tested version of `pip` to avoid getting the latest one
in case it's broken (this has happened before a few times).

    :::docker
    FROM python:3.7.8-alpine

    RUN wget -q https://bootstrap.pypa.io/get-pip.py \
        && python3 get-pip.py pip==19.1.1 \
        && rm get-pip.py

    COPY app/requirements.txt ./

    RUN pip install -q --no-cache-dir \
        -r requirements.txt \
        && rm requirements.txt

Given that the `requirements.txt` contains `pytest` and the `app` folder has modules with test
functions, you should be able to run `pytest` against the mounted directory:

    :::bash
    $ docker run --rm -v ${PWD}/app:/opt/project/app snake pytest /opt/project/ -v
    # pytest output 

Because your current working directory is mounted as a volume, the files generated by
the commands you run will be available on the host.
This means you can run the `coverage` command in the Docker container and the `.coverage`
file will be available on the host.
Given this file, you'll be able to generate the HTML report to view in your host's web browser.

### Make host environment variables available in a Docker container

It is common to use environment variables for storing some settings that Python programs
may depend on.
Keep in mind that a more robust strategy for storing sensitive information is to use 
[Docker secrets](https://www.docker.com/blog/docker-secrets-management/).


    :::docker
    FROM python:3.7.8-alpine

By default, host's environment variables (both permanently stored and temporarily exported) are not
available in a Docker container.

Given this Python program,

    :::python
    import os
    print(f'Token: {os.getenv("SITE_TOKEN")}')

you can run it in a Docker container:

    :::bash
    $ export SITE_TOKEN='mytoken'
    $ docker build -t snake .
    $ docker run -v ${PWD}/app:/opt/project/app snake python3 /opt/project/app/main.py
    # Token: None

The `-e` (`--env`) parameter will let you specify the environment variables you want
to propagate into the Docker container.

    :::bash
    $ export SITE_TOKEN='mytoken'
    $ docker run -e SITE_TOKEN=${SITE_TOKEN} -v ${PWD}/app:/opt/project/app snake \
        python3 /opt/project/app/main.py
    # Token: mytoken

### Attach to a running Docker container

When running a Python program in a Docker container in debugging mode, 
it can be useful to be able to pause the program and connect to the container
to be able to inspect the file system.

A few IDEs such as PyCharm and VSCode provide support for remote Python debugging
and will be able to start a Docker container running a Python program and then
later tell you its id.
This is especially useful when the Python program is expected to produce some files
and you would like to inspect them to verify the program produces correct results.

If you know the container id, you can attach to it with:

    :::bash
    $ docker exec -it <container_id> /bin/bash

If you don't know the container id, you will need to get it first which can be done with:

    :::bash
    $ docker ps --filter status=running

The `CONTAINER ID` field will contain the id of the Docker container you will need to attach to.
If you have multiple running containers, the one you need is likely to be the first one in the list.

Happy containerization!