title: Adding a dependency to your Python project: a practical guide
date: 2021-06-19
modified: 2021-06-19
author: Alexey Tereshenkov
tags: python, build-systems
slug: adding-python-dependency
category: python

[TOC]

After managing Python projects for quite a few years now, I've learned several things one should think about when bringing a 3rd party dependency to a project. In this post, I'll cover some of the points that are worth considering when deciding to rely on code external to your organization. This post is concerned with a long-living code that is part of a larger piece of software and not a throw-away one-time use Python script to which these concerns do not apply.

## What are the consequences of bringing external dependencies?

When your software starts depending on the 3rd party packages:

* it takes longer to build a project (downloading and resolving dependencies)
* you become dependent on an external project that is not guaranteed to be maintained or developed
* the risks of having incompatible dependencies is increased (particularly when you have multiple external dependencies each having an extensive number of dependencies)
* upgrading versions of other external dependencies may be more brittle due to potential dependencies conflicts

Before bringing in an external dependency, it may be helpful to find out whether it is really needed. In a general case, I believe it's useful to be reluctant to adding any external dependencies unless the benefits of bringing them outweigh the associated cost.

If the Python program you write can complete a task without using any 3rd party code, keep it that way. Any code that you haven't written yourself (or is not originated and maintained within your team or organization) that becomes part of your software adds additional risks and maintenance costs. Using a Python library may indeed save development time for the team, however, adding a new dependency should be justified; very often it may not be worth it. 

Say your program needs to read an input `.csv` file, apply some filter on the data rows, and produce a new `.csv` file with a subset of the original one. `pandas` library would make doing this very easy -- this could likely be done in a single line of code. However, unless the program needs to read very large files and do it very often (so there are some performance constraints), you are better off using Python standard library [csv](https://docs.python.org/3/library/csv.html) module that makes working with `.csv` files fairly easy.

In contrast, when writing a new machine learning library, it would be a pity not to take advantage of existing numerical computation libraries such as `numpy` and `scipy` because they are likely to be core foundation of the project. In this case, it is very unlikely that you would need to implement own data structures that would meet the functional and performance requirements of your project, and overall be a better solution than an existing battle tested library.

## Explore the external dependency

When you have identified a dependency to bring in, it may be worth spending some time learning more about it. Do the research and explore [Snyk Advisor](https://snyk.io/advisor/python/pandas), the [project's source code repository](https://github.com/pandas-dev/pandas), code quality [reports](https://lgtm.com/projects/g/pandas-dev/pandas), and the [PyPI project page](https://pypi.org/project/pandas/) to learn more about the project.

### Library maintenance status and release cadence

High commit frequency would indicate active development, and projects that are actively developed are more favorable than stale ones.

### Number of downloads from the PyPI

This should give an idea whether the project is used by other organizations and individuals. 

### Any known security issues and vulnerabilities

If this is applicable, you may want to explore any reported security issues or use static analysis tools before deciding whether to take in a dependency or not.

### Developer community

A project with a single contributor can be considered to be less reliable than a project with multiple contributors - what happens if the only maintainer leaves the project?

### Reported issues

The number of issues is likely to be proportional to the project popularity, but it's possible to get an idea whether project authors are responsive and work on resolving issues.

### Python version compatibility

If a library of interest uses features of Python 3.9, you may not be able to use it in Python 3.6 environment. There may be a backport of the future Python version functionality for an older version (such as [dataclasses](https://pypi.org/project/dataclasses/)), but it may still stop you from embedding the external library if it is not supported on the version of the target Python runtime environment.

### Dependencies

A project with no (or fewer) external dependencies is easier to integrate than a project with extensive number of external dependencies. Each dependency brings alone its own (transitive) dependencies which increases the chances of dependencies conflicts at dependency resolution time.

### Licensing

A 3rd party package license may or may now allow further distribution of the code or using it in a commercial product.

### Distribution formats

Having only source distributions (`sdist`) may imply that you may need to build the wheel(s) (`bdist_wheel`) to make a binary distribution accessible for your own project build process. Unless you are able to build the wheels yourself and make them available via a binary repository manager such as a hosted PyPI repository or in some other way, libraries with wheels published on PyPI are more preferable.

### Source code programming languages 

Having a [non-pure Python package](https://packaging.python.org/guides/distributing-packages-using-setuptools/#pure-python-wheels) with certain bits written in a compiled language such as C or Rust would make building binary distributions harder since you'll need to have the necessary toolchain set up and may imply building multiple wheels for each target platform and/or architecture.

## Adding the dependency

If after evaluating a library you have decided to bring it into your Python project, you would need to declare that dependency. The way you do it would depend on your dependency management approach - this may be done via a number of ways such as by using a requirements file, a Poetry project file, or a Pants/Bazel project file. Ideally, [constraints file](https://pip.pypa.io/en/stable/user_guide/#constraints-files) is used to make sure that the same versions of all the transitive dependencies of a project are used, even when a new version of the 3rd party library will be released.

The reality is that for any Python project of decent size and complexity it may be difficult to not use 3rd party code. The necessity to add a dependency should be discussed within the team. If there are multiple libraries that provide functionality of interest, write a document that would let you compare them based on the criteria I've mentioned above. Bringing in external dependencies is an important step for your project and should be done with care and planning.

Happy depending!