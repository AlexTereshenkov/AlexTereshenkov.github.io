title: What I think about programming QA forums
date: 2020-11-29
modified: 2020-11-29
author: Alexey Tereshenkov
tags: tech-support
slug: programming-qa-forums
category: tech-support
status: draft

[TOC]

## Overview

Writing code these days is a lot easier in many regards at least because it's much easier to
get help if you are stuck. 
When you get an error running a program, after giving it a thought and looking around the source code,
I think most of us would do an online search.
There is even a joke about being a 
[Full StackOverflow developer](https://www.reddit.com/r/ProgrammerHumor/comments/d0dyln/fullstackoverflow_developer/).
This is so because most often you'd be able to find most relevant results online.
When you have figured out the solution, I find it to be very helpful to get to the docs
and then read more about the particular error message if it was documented as well as 
about the concepts that are involved.

## A chance to learn

I think it's very tempting to continue coding immediately after you have fixed the problem 
(by finding the problem explanation and the solution online),
but I think you'd miss a great opportunity to learn more.
This is because learning about the concept right when you are facing a related issue is perfect in terms of timing.

Let's say you run a Python program and you get a `SyntaxError` in a line with an f-string.
You search online and found a post by someone who also had this issue and people told them
that f-strings are added to Python 3.6 and are not supported in lower versions.
You say "ah, of course!" and fix the shebang line of your Python program to be `#!/usr/bin/python3`
instead of `/usr/bin/python`.
You can continue coding as you are unblocked.
But I'd pace myself and would try to learn more (when time permits).

* What is the shebang line and how does it work? 
* Is it possible to port f-strings to use in Python 2?
* How do I make sure that my Python programs will be run on Python 3.6+ in production (and not be mistakenly run on Python 2)? 
* Do we need to support earlier versions of Python at all? 
  If so, how do we write and run tests to be sure that our code is backwards compatible?

Getting answers to all those questions is very helpful.
It's hard to come up with all those questions at an arbitrary point of time, but is extremely easy to think of them
while you are dealing with a related problem.

## Using QA forums

Given how many different frameworks, technologies, and programming languages a software engineer may need to use on a daily basis,
I think it would be counterproductive not to take advantage of the sheer amount of resources that QA forums under the 
StackExchange umbrella (such as StackOverflow.com) are offering.

If a person is a zoologist who needs to filter out some records in a .csv file and they are in a rush,
I don't see a particular problem helping them by providing a working solution.
Isn't it about being useful to others and being able to apply your skills for the good?

## 

Happy helping!
