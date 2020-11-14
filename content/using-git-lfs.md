title: Brief overview of using Git LFS for managing binary files
date: 2020-11-13
modified: 2020-11-13
author: Alexey Tereshenkov
tags: git,lfs
slug: overview-using-git-lfs-binary-files
category: git

[TOC]

## Overview

Normally a Git repository is used to manage source code which is stored most often as plain text.
Tracking changes for text is very easy because only the changes between two commits would need to be
saved, not the whole copies of the files.
However, a project source code repository may also contain binary files such as images, compiled code, or
archives.

Developers from quite a few industries such as gaming or computer-aided design and digital mapping
(e.g. textures, CAD drawings, and map style files) often have to manage and store large files.
Having files of a few megabytes or hundreds of megabytes in size can be very common in 
the project source code repository, however, there is nothing wrong with having them there
since this is where they really belong.

## Problem of keeping binary files under Git

Because Git cannot track changes between binary files, for each modification of a binary
file, a copy of the modified file will be created and stored.
This can make the repository unnecessary large and slow to clone and check out.
Always overwriting the binary file with the latest file state (to keep only the "latest") 
defeats the purpose of the source code management as one should be able to have access to the
history even if it implies storing a hundred of binary files each differing from others by just
a few bytes.

What is a large file is a subject for discussion.
I'd also encourage to think about how often a binary file will change; 
if it's a couple of megabytes static image used in a background of your terminal app, 
you may be fine just storing it as is.
If it's a dynamic file that will be modified daily by multiple developers, just half a megabyte
digital drawing file can bloat the repository for all of time if it's modified often.
Having many tiny binary files that are changed often can have a similar effect.

## Using Git LFS for tracking binary files

A more efficient way to store the binary files is to store them not under the Git repository
(when a change to a binary file will cause creating its full copy),
but in a separate storage system such as [Git LFS](https://git-lfs.github.com/).
This system lets you store in the Git repository only the pointers to versions of the binary files,
whereas the files themselves are stored separately.
When cloning the repository with the latest `master`, 
you will only need to download the latest file, not its whole history.
When checking out a `feature-branch` (that may have another representation of the very same file),
another file version will be downloaded.

Most of the major source code management providers such as GitHub, GitLab, and BitBucket provide
support for Git LFS and enabling it is extremely easy.
To learn more about Git LFS and support for large objects in Git, see the excellent video
[Native Git support for large objects](https://www.youtube.com/watch?v=0sRHRMp-Bpc) from the Git Merge 2019.

## Migration of files to LFS

The decisions about management of the binary files should be made as early as possible when
setting up the repository.
This is because it's a lot easier to start using Git LFS when a new repository is created rather
than when binary files have already sneaked into the Git history.
Ideally, you shouldn't be tracking with Git binary files that are supposed to be modified often.
If the files did sneak into the Git history, simply removing the files and then starting storing them
in a separate LFS system won't be enough as the Git repository will still have copies of those
binary files in the history (in the `.git` directory).

It is possible to remove them completely, but this would require 
["rewriting" the history](https://darekkay.com/blog/git-rewriting-history/) and would 
require careful coordination with anyone else using the repository to run a few `git rebase --onto` sessions.
For a repository with a few branches used by a few developers this won't be a problem, but it can become
impractical and plain tedious to migrate the files for a large repository with many contributors and
many branches.

If you do need to move the files out of a "regular" Git to the LFS system, refer to the
[Migrating existing repository data to LFS](https://github.com/git-lfs/git-lfs/wiki/Tutorial#migrating-existing-repository-data-to-lfs) 
page section in the Git LFS tutorial.

Happy storing!
