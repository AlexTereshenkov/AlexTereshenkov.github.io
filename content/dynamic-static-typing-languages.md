title: Thinking about programming languages with dynamic and static type system
date: 2021-07-25
modified: 2021-07-25
author: Alexey Tereshenkov
tags: computer-science,programming
slug: dynamic-static-typing-languages
category: computer-science

[TOC]

After writing programs for a while in several programming languages, both professionally and for learning, I started thinking about benefits and drawbacks of programming languages with dynamic and static type systems. As with many other aspects of the software engineering industry, there are developers advocating for using interpreted, dynamically typed languages such as Python[^python-interpreted]. Likewise, there are ones who wouldn't consider using such a language for anything other than a minor script or a utility program and rather stick to compiled, statically typed languages such as C++ and Java[^java-compiled].
In this post, I'd like to outline my considerations and share some thoughts and personal experiences. Given that I am mostly familiar with Python and Java, I'll use these two languages when reasoning about the use cases.

## Interpreted vs compiled languages

### Speed of development

When there isn't a lot of time available for development or when the business requirements are not clear (so it's important to be able to make future changes easily), a team may decide to use an interpreted language. It becomes possible to complete writing a program significantly faster, however, the performance of an interpreted program will likely be worse. This is not necessarily a negative thing if the program run time is acceptable given the performance constraints, if any.

### Rapid prototyping

Being able to complete an initial prototype fast makes an option to use a dynamic language very attractive. There may be a need to redo the implementation completely -- plan to throw one away; you will anyhow[^brooks]. It is suggested to prototype in an interpreted language before coding in a compiled language such as C[^raymond-prototype] because general-purpose scripting languages make it very easy to construct framework of a program relying on external tools only when there is a special-purpose task[^practical-scripting]. There has been a claim that code can be written 5 to 10 times faster in a scripting language, but would run 10 to 20 times faster in a traditional compiled systems language[^Ous98]. An approach to implement a performance critical parts in a compiled language leaving the rest of the code in a dynamic language is so ubiquitous that perhaps the argument that dynamic languages shouldn't be used because they are "slow" is not relevant any longer.

### Suitability

If most developers would probably agree on the prototyping story of scripting languages, what about writing a sophisticated piece of software with a dynamic language? Some of these languages were created for purposes other than building complex production software such as to teach programming, write short text-processing utilities, or be a glue language to integrate existing programs within a larger system. Some of the dynamic languages, however, were intended by their designers for general-purpose use, to support "programming in the large"[^practical-scripting]. However, as the size of the software increases, so often does the complexity of source code management. What often is taken in a statically typed, compiled language for granted (type checking, project-wide refactoring tools, dependency inference) becomes harder and harder when using a dynamically typed, interpreted language.

### Type safety

Type annotations have been introduced to Python fairly recently and there are many code bases which are still not typed or typed only partially. Lots of software written in Python was written by professionals in adjacent domains such as engineering, finance, and data science. Those open-source projects often lack a vigorous build pipeline that would be considered a norm in a statically typed language commercial setting (code coverage, linting, static analysis). Therefore, I think in the eyes of Java developers, many large Python projects may look less mature and less robust for this very reason. When experimenting using a Python framework and getting a runtime type error, a programmer writing in a statically typed, compiled language may thus find a dynamic language not suitable for large scale development.

## Succeeding developing in dynamically typed language

However, I believe it is possible to write great software with a dynamically typed, interpreted language. To be able to do that, a few things are required.

### Expectations

Set the same expectations for programs written in a dynamically typed language that are set for programs written in a statically typed language. The programs written in Python can be made much easier to maintain and reason about if they follow the software engineering best practices which can be drawn from various sources (e.g., [source code complexity](https://rules.sonarsource.com/python/tag/brain-overload), [readability](https://google.github.io/styleguide/pyguide.html), and [type safety](https://dropbox.tech/application/our-journey-to-type-checking-4-million-lines-of-python))

### Design principles

Apply the design principles and implementation restrictions from statically typed languages in your dynamically typed language. For example, Java won't let you define multiple classes in the same file, so make sure in your Python project, you put only closely related units of work into a single file.
[MISRA C guidelines](https://pvs-studio.com/en/docs/warnings/v2565/) prohibit using recursion, so make sure you don't use [recursion](https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it) in your Python programs.
Strongly and statically typed languages force you to specify the method return type, so you may want to make sure all your [Python functions have a return type](https://mypy.readthedocs.io/en/stable/existing_code.html#introduce-stricter-options).

### Aggressive build pipeline

In line with the DevOps practices, when building a project in CI, the build pipeline should be looking for reasons to reject a build. If any of the steps - formatting, linting, spell checking, testing, type checking -- fails, the code coverage percentage goes down, or in case of any other declared event, then the build fails and the code can't be merged. This principle of "Reject it"[^release-it] is applicable to any programming language, of course, but is particularly relevant for dynamic languages given the flexibility they provide.

There are a few examples of highly successful Python projects that follow the principles outlined above such as the [wemake-services Python linter](https://github.com/wemake-services/wemake-python-styleguide) and [Pants build system](https://github.com/pantsbuild/pants).

## Conclusion

An argument against enforcing stricter development constraints for a dynamic language could be raised. It may indeed take longer time to produce a program where all function parameters and return values have type annotations, variables with the same name are not declared multiple times, and public methods have docstrings. There is no point in such vigorous approach when prototyping, however, as soon as the code is integrated into some bigger unit, the expectations should get higher. 

Writing robust, easy to extend and maintain _large_ software in Python isn't going to be a whole lot faster than writing it in Java. I believe Python should be chosen to be the language of implementation for reasons other than speed of development (even though it may often be the case), but because of its expressiveness, extensive built-in library and public package repository, community and tooling. The lessons learned about the program design, modularization, and code health when building large scale commercial, enterprise, or open-source software in compiled languages should be explored by dynamic language developers. Having many successful products created in dynamic languages, it is for certain that writing large programs in dynamically typed languages is very much possible. In the end, typing system doesn't define the success of a software product; it's all about the development processes and people.

[^python-interpreted]: Python can also be said to be compiled given the program's source code is first compiled into bytecode, but we can omit this detail to make the distinction clearer.
[^java-compiled]: Java can be said to be either interpreted or compiled, but we can omit this detail to make the distinction clearer.
[^brooks]: Brooks, F.H. The Mythical Man-Month, Addison-Wesley, 1975.
[^raymond-prototype]: Eric S. Raymond. The Art of Unix Programming, Addison-Wesley, 2003.
[^practical-scripting]: Michael L. Scott. Programming Language Pragmatics, 4th edition, Elsevier, 2016.
[^Ous98]: John K. Ousterhout. Scripting: Higher-level programming for the 21st century. IEEE Computer, 31(3):23-30, March 1998.
[^release-it]: Michael T. Nygard. Release It!, 2nd Edition, January 2018.