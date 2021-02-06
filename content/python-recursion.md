title: Introducton to recursion with Python
date: 2021-02-06
modified: 2021-02-06
author: Alexey Tereshenkov
tags: python,recursion,functional-programming
slug: python-recursion-intro
category: python

[TOC]

## Overview

Recursion can be one of the programming concepts that can be a bit of a challenge
to understand.
I believe this is because the recursive call to a function is not written in a
procedural way so that one cannot see the actual sequence of operations that will
be taken.
Running a program containing a recursive function call with a debugger to be able
to step through each line can be very useful.

I've spent a few weeks learning [ML](https://en.wikipedia.org/wiki/ML_(programming_language))
and was fascinated by the recursion implementation in functional languages and ML in particular.
It can be mind bending for anyone who has learned programming through non-functional
programming languages that do not encourage use of recursion be it Python or Java.
However, I had quite a few "aha!" moments when writing recursive functions in ML
and I definitely understand recursion much better now.

In this post, I wanted to share a few simple recursive functions that are 
written in Python.
I believe practicing writing recursive functions is fun and is a great 
mind-expanding exercise.

## Declarative iterations or recursions?

I believe the consensus about recursion is that it's appropriate to use recursion
in situations when a recursive solution would be better expressed in a recursive call.
That is, there isn't a problem that can't be solved without using recursion or if there is one,
it must be so rare you'll probably never face it.

However, it's very useful to know what recursion is to be able to understand the code
that others have written and the caveats associated with using recursion in 
your programming language.

Let's take a look at a few simple cases.

## Examples of recursive functions

If you run any of the of the programs below (each featuring a recursive function call) 
in a debugger to be able to step through it, 
you'll see that for each recursive function call, a new 
[frame is added on stack](https://runestone.academy/runestone/books/published/pythonds/Recursion/StackFramesImplementingRecursion.html).

Python imposes a limit on the number of the recursive calls (
see [maximum recursion depth](https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it)) which guards against a stack overflow.
This means that for most of the real life data, it won't be safe to use the examples below.
This is why it can be useful to recognize a recursive call and evaluate whether it's safe to use or not.
The [coding guidelines](https://www.viva64.com/en/w/v2565/) for some industries may even explicitly ask 
to avoid using recursion and replace it with a loop or an iterative algorithm.

You can also attempt to solve these tasks as an exercise before looking at my solutions.
Each function has a [doctest](https://docs.python.org/3/library/doctest.html) 
which you can use to check your understanding of the problem.
The problems are sorted by difficulty in ascending order.

### Sum values in an array of integers

Given an array of integers, find the sum of all its elements.

This can be solved by simply using the built-in `sum()` which is what most
Python developers would use:

    :::python
    sum([1,2,3,4,5])

However, this task can also be solved using a simple `for` loop and a result variable:

    :::python
    total = 0
    for number in [1,2,3,4,5]:
        total += number
    print(total)
    # 15

And of course, a recursive solution can be written as well:

    :::python
    def sum_list(values):
        """Sum values in an array of integers.
        >>> sum_list([])
        0
        >>> sum_list([1])
        1
        >>> sum_list([1,2,3,4])
        10
        """
        if len(values) == 0:
            return 0
        elif len(values) == 1:
            return values[0]
        else:
            return values[0] + sum_list(values[1:])


The way I used to reason about this function call is that I decompose the result of each recursive call
which can be helpful to understand what is going on.
The way I see the line `return values[0] + sum_list(values[1:])` for the initial array of `[1,2,3,4]` is

    :::text
    1 + sum_list([2,3,4]) =>
        1 + (2 + sum_list([3,4])) =>
            1 + 2 + (3 + sum_list([4])) =>
                1 + 2 + 3 + 4 => 10

### Produce range of integers

Given a positive integer, produce a list of integers from the given integer down to 0.

    :::python
    def countdown(num):
        """Get a list of integers from the given 
        positive integer down to 0.
        >>> countdown(5)
        [5, 4, 3, 2, 1, 0]
        """
        if num == 0:
            return 0
        elif num == 1:
            return [1, 0]
        else:
            return [num] + countdown(num-1)

### Merge two arrays of items

Given two arrays of items, merge them into a single array keeping the order of items.

    :::python
    def merge(arr1, arr2):
        """Merge two arrays of items.
        >>> merge([1,2,3], [4,5,6])
        [1, 2, 3, 4, 5, 6]
        >>> merge([1,2,3], [])
        [1, 2, 3]
        >>> merge([], [4,5,6])
        [4, 5, 6]
        """
        if not arr1:
            return arr2
        else:
            return [arr1[0]] + merge(arr1[1:], arr2)

### Sum integers in a list of pairs

Given an array of non-empty pairs (with each pair containing two integers), 
find the sum of all numbers in the array.

    :::python
    def sum_list_of_pairs(arr):
        """Sum integers in a list of pairs.
        >>> sum_list_of_pairs([])
        0
        >>> sum_list_of_pairs([(1,2)])
        3
        >>> sum_list_of_pairs([(10,20), (30,40), (50,60)])
        210
        """
        if not arr:
            return 0
        else:
            return arr[0][0] + arr[0][1] + sum_list_of_pairs(arr[1:])

### Get first elements of sub-arrays in array

    :::python
    def firsts(arr):
        """Get first elements of all collections in a given array.
        >>> firsts([])
        []
        >>> firsts([(1,2,3), (4,5,6)])
        [1, 4]
        >>> firsts([(1,2), (3,4), (5,6)])
        [1, 3, 5]
        """
        if not arr:
            return []
        else:
            return [arr[0][0]] + firsts(arr[1:])

## Tail recursion optimizations

A special, perhaps more difficult concept to understand, is tail recursion.
The recursive functions we have above have a pattern in the `return` statement.
They return a value and the call to itself (such as `return array[0] + func(array[1:])`)).
However, if a function would only call itself recursively and wouldn't need to keep any intermediate data,
it would be considered a tail recursive function.
That is, since there is no intermediate data to maintain (which is why the stack frames are needed),
we can essentially replace the current stack frame where the function is calling itself with the new stack frame
since we don't need to get back to it -- we would only be interested in the final recursive call that would
have the final value we need.

### Factorial of a positive integer

This function is not tail-recursive because we need to maintain the value of `n` that we
will multiply with the result of `factorial(n-1)`.

    :::python
    def factorial(n):
        """Get factorial of n.
        >>> factorial(0)
        1
        >>> factorial(5)
        120
        """
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)

The reason we would want to make our function tail-recursive is because some programming languages provide
what is called a [tail call optimization](https://stackoverflow.com/questions/310974/what-is-tail-call-optimization).
This is how a functional programming language such as 
Scala supports hundreds of thousands recursive function calls, see [here](https://alvinalexander.com/scala/fp-book/tail-recursive-algorithms/).

Python does not have tail call optimization 
([here's why](https://stackoverflow.com/questions/13591970/does-python-optimize-tail-recursion)), 
but let's rewrite the factorial function in a tail-recursive fashion anyway to practice.

The idea around tail-call optimization is to use some kind of accumulator, 
the `acc` parameter in the example below, that tracks the intermediate data 
and is passed across the subsequent calls thus eliminating 
the need to keep the previous stack frames.

    :::python
    def factorial_tail(n, acc):
        """Get factorial of n in a tail-recursion fashion.
        >>> factorial_tail(0, 1)
        1
        >>> factorial_tail(5, 1)
        120
        """
        if n == 0:
            return acc
        else:
            return factorial_tail(n-1, acc*n)


Let's write a few more examples of functions with tail call.

### Sum values in an array (tail call)

    :::python
    def sum_values_tail(arr, acc):
        """Sum values in an array in a tail-recursion fashion.
        >>> sum_values_tail([1,2,3], 0)
        6
        >>> sum_values_tail([], 0)
        0
        """
        if len(arr) == 0:
            return acc
        else:
            return sum_values_tail(arr[1:], arr[0]+acc)

### Reverse an array (tail call)

    :::python
    def reverse_list_tail(arr, final):
        """Reverse list in a tail-recursion fashion.
        >>> reverse_list_tail([], [])
        []
        >>> reverse_list_tail([1], [])
        [1]
        >>> reverse_list_tail([1,2,3], [])
        [3, 2, 1]
        """
        if len(arr) == 0:
            return final
        else:
            return reverse_list_tail(arr[1:], [arr[0]] + final)

### Reduce (tail call)

    :::python
    def reduce_tail(func, acc, arr):
        """Reduce (fold) an array to a single value applying a function.
        >>> reduce_tail(lambda x,y: x * y, 1, [1,2,3,4])
        24
        >>> reduce_tail(lambda x,y: x + y, 0, [1,2,3,4])
        10
        """
        if len(arr) == 0:
            return acc
        else:
            return reduce_tail(func, func(acc, arr[0]), arr[1:])

## Mutual recursion

Another more advanced concept is mutual recursion which is a type of recursion 
when two functions are defined with referral to each other.

In this example, given an array of integers, we want to check if it follows a certain
pattern, `[1,2,1,2...1,2]` in this particular case.
Once the function responsible to confirm that the first item of the array is `1` is done, 
it calls another function that confirms that the first item of the array is `2`, 
and then it calls the first function that confirms that the first item of the array is `1` and
the cycle repeats.

    :::python
    def pattern_match_one_two(arr):
        """Check if a sequence is a pattern 1,2 repeated
        using a mutual recursion.
        >>> pattern_match_one_two([1,2,1,2,1,2])
        True
        >>> pattern_match_one_two([1,2,1,2,3,1,2])
        False
        >>> pattern_match_one_two([2,1,2,1,2])
        False
        """
        if len(arr) == 0:
            return True
        else:
            if arr[0] == 1:
                return needs_two(arr[1:])
            else:
                return False


    def needs_two(arr):
        if len(arr) == 0:
            return True
        else:
            if arr[0] == 2:
                return pattern_match_one_two(arr[1:])
            else:
                return False

---

Hope this short introduction helped you understand recursion better 
and you find the code examples illustrative and useful.

Happy recursive coding!
