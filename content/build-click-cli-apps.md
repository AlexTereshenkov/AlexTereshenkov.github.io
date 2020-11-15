title: Building cli Python applications with Click
date: 2020-11-15
modified: 2020-11-15
author: Alexey Tereshenkov
tags: python,click,cli
slug: building-cli-python-apps-with-click
category: python

[TOC]

## Overview

When writing cli tools using Python, if the complexity is low, using a plain `argparse` may suffice.
Despite being a built-in module, it's still very capable and relatively flexible.
In fact, a few large open-source projects have survived using `argparse` without using any custom
cli frameworks.
For instance, 
[Conan](https://github.com/conan-io/conan/blob/develop/conans/client/command.py) 
-- a popular C/C++ package manager written in Python -- 
and [Google API Client for Python](https://github.com/googleapis/google-api-python-client) 
-- Google's discovery based APIs -- are using `argparse` for their cli interfaces.

When `argparse` limitations get in the way, you may start looking for [Python frameworks 
that allow developing cli applications](https://docs.python-guide.org/scenarios/cli/).
There is a post with practical demonstrations of most popular Python cli frameworks
that is worth reviewing: [Building Beautiful Command Line Interfaces with Python](
https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df).

## Building a cli with Click

My personal preference for a Python cli framework is [Click](https://click.palletsprojects.com/en/7.x/).
It has the functionality I want to have when building cli applications 
and whenever I needed something a bit peculiar, I was able to find the answers online thanks to
posts of [Stephen Rauch](https://stackoverflow.com/users/7311767/stephen-rauch?tab=answers).

To save time for others, I've created a boilerplate repository -- 
[`click-cli-boilerplate`](https://github.com/AlexTereshenkov/click-cli-boilerplate) --
that contains everything
that one would need to get started developing a cli application using `Click`.
It features the Python project source code layout, cli interface and implementation relation, 
tests, packaging, and docs generation.
You will find some brief notes on how to write tests, how to generate the docs using the
[sphinx-click](https://github.com/click-contrib/sphinx-click) extension, and how to distribute
the cli application as a Python wheel and let users install it with the `pipx`.

Happy cli-ing!
