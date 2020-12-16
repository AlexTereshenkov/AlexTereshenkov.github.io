title: Some helpful Bash notes
date: 2020-12-15
modified: 2020-12-15
author: Alexey Tereshenkov
tags: bash,linux
slug: some-helpful-bash-notes
category: bash

[TOC]

## Overview

There are quite a few resources online on Bash scripting which are extremely useful.
I particularly recommend [Awesome Bash](https://github.com/awesome-lists/awesome-bash) and 
[The Art of Command Line](https://github.com/jlevy/the-art-of-command-line).
There is little point writing yet another Bash tutorial, however, I'd like to share
a few helpful notes which others who just start using a command line 
may find useful.

### Multiple arguments to the same command

Many Unix commands accept multiple arguments, one after another:

    :::bash
    $ ls *.jar *.vsix
    tmp-142zodmSW1YLvRv.vsix    tmp-417e1PTGYuSLOnV.vsix  winstone10385665803316081333.jar
    tmp-192iFDUu55RqcPk.vsix    tmp-417qbhJlHnXzkZl.vsix  winstone4439219046698760640.jar
    tmp-31894bwaoyq9zL7em.vsix  tmp-549k8JeuzrFyHMC.vsix  winstone4470366079702491377.jar

    $ touch foo.bar foo.baz
    $ ls foo.*       
    foo.bar  foo.baz

### One line `for` loop

It's common to see a `for` loop that spans over multiple lines in shell scripts:

    :::bash
    for jarfile in *.jar;
      do file ${jarfile};
    done

However, working with the `for` loop spanning over multiple lines in terminal
can be cumbersome.
Fortunately, the `for` loop can be put into a single line:

    :::bash
    $ for jarfile in *.jar; do file ${jarfile}; done
    winstone10385665803316081333.jar: Java archive data (JAR)
    winstone4439219046698760640.jar: Java archive data (JAR)
    winstone4470366079702491377.jar: Java archive data (JAR)

### Reading standard input

Some programs are limited and may not accept files as input arguments.
Another use case is when you have to pass sensitive data such as passwords
as input to programs using a command line interface (so that it doesn't
end up in the terminal history).

For example, you may need to produce a semicolon separated list of files
(and some program has already produced a list of files):

    :::bash
    $ cat files.txt
    winstone10385665803316081333.jar
    winstone4439219046698760640.jar
    winstone4470366079702491377.jar

    $ tr '\n' ';' < files.txt
    winstone10385665803316081333.jar;winstone4439219046698760640.jar;winstone4470366079702491377.jar;%

### Submit multiline input to a command

When you need to supply a multiline input to a command, particularly if this needs to happen interactively,
you can use a [here document](https://en.wikipedia.org/wiki/Here_document) 
which can be used within a shell script file or at a prompt:

    :::bash
    $ tr '[:lower:]' '[:upper:]' << END
    first line
    and second line
    and third line
    END

    FIRST LINE
    AND SECOND LINE
    AND THIRD LINE

Another useful feature is to be able to write multiline input to a file.
This can be very handy when you have to create a multiline file 
(potentially with non trivial indentation) and the machine you are connected to 
does not have any text editors available.

    $ cat << EOF > dummy.txt
    The file contents to be written: line 1
    and line 2
    EOF

    $ cat dummy.txt             
    The file contents to be written: line 1
    and line 2

### Single and double quotes

Single quotes do not let filename and variable expansion to happen in the quoted text.
Be very careful mixing the single and double quotes!

    :::bash
    $ export SITE_TOKEN='mytoken' 
    $ echo "$SITE_TOKEN"        
    mytoken
    $ echo '$SITE_TOKEN'
    $SITE_TOKEN

### Grouping commands and values using curly braces

It can be very useful to be able to run multiple commands, one after another,
and save the output to a file.
This would let you avoid having multiple lines in your script (where each line would be 
appending to the file).
For instance, to create a log of some system operation:

    :::bash
    $ { date; whoami; echo "----"; ls /var } > log$(date '+%Y-%m-%d').txt

    $ head -n 5 log2020-12-15.txt 
    Tue Dec 15 22:21:59 GMT 2020
    username
    ----
    backups
    cache
    crash

Happy shelling!