title: Querying metadata of a zip file over network
date: 2024-12-17
modified: 2024-12-17
author: Alexey Tereshenkov
tags: python
slug: query-zip-metadata-with-python
category: python

[TOC]

## Introduction

I recently had to download some data files from a web service. The data was split across multiple archive files, there was no metadata on the contents of the archive files published, and each file was multiple gigabytes in size. Imagine you need some statistical data for a particular country in Europe, but this dataset is in one of the hundred files available. I started wondering whether there's a better approach than to download all of the files over a few days (there may be download speed restrictions), unpack each of them, and find out which directory has dataset I am looking for (based on the filename).

## Problem

Even though this was a personal project, I thought it wouldn't hurt to attempt to address this from the software engineering perspective. A naive solution to this as I said would be to download all of the files, however, imagine this needs to happen in CI for every build or daily on a developer machine (as the data may be updated often). This clearly won't scale -- it's going to be both slow (network access) and resource intensive (depending on the compression and nature of data, unpacking may require a lot of disk space).

Since the name of the file is known, I got curious about sending queries to the archive files without downloading them completely. I discovered this is possible with [HTTP range requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) which let clients request from server only parts of a resource. Luckily the server I was interacting with did support the range requests (not every server does, apparently) so now we can download a piece of every zip file which helps, but how do I know what part to download?

## Solution

Because the data was stored in [zip files](https://en.wikipedia.org/wiki/ZIP_(file_format)) and this format has a formal specification with the metadata about its contents available, we can send byte-range requests to only download certain bytes (known beforehand) from each archive file. Here's a basic Python script I wrote to check what archive file I actually need to download:

```python
import requests
import zipfile
from io import BytesIO


def send_range_request(url: str, start: int, end: int) -> bytes:
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers, stream=True)
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/206
    return response.content


def main(url: str):
    # Get the first 4 bytes to read the file signature
    header = send_range_request(url, 0, 3)
    # Magic number that is part of the zip file format spec
    assert header == b'PK\x03\x04'

    # Get the total file size
    file_size = int(requests.head(url).headers['Content-Length'])

    # Get the last 22 bytes to locate the central directory;
    # default size of 'End of central directory record' (EOCD)
    eocd = send_range_request(url, file_size - 22, file_size - 1)

    # Parse the EOCD record
    eocd_signature = eocd[:4]
    # Magic number that is part of the zip file format spec
    assert eocd_signature == b'PK\x05\x06'

    # Size of central directory
    cd_size = int.from_bytes(eocd[12:16], byteorder='little')
    # Offset of start of central directory
    cd_offset = int.from_bytes(eocd[16:20], byteorder='little')

    # Load the central directory into a zip file object;
    # having just this much metadata is actually enough to construct
    # a valid zip file from the set of bytes
    zip_data = send_range_request(url, cd_offset, file_size)
    zip_file = zipfile.ZipFile(BytesIO(zip_data))

    # For illustration, list C source files inside the numpy package
    for f in zip_file.namelist():
        if f.endswith(".c"):
            print(f)

    print(f"File size: {file_size} bytes")
    print(f"Downloaded metadata: {cd_size} bytes")
    print()
```

For illustration, we could run this script to list some files inside Python wheels which are zip files:

```python
# numpy package, Python wheel file (that is just a zip file)
url_numpy_win32 = (
    'https://files.pythonhosted.org/packages/d4/dc/'
    '09a4e5819a9782a213c0eb4eecacdc1cd75ad8dac99279b04cfccb7eeb0a/'
    'numpy-2.2.0-cp313-cp313t-win32.whl'
)
url_numpy_macos = (
    'https://files.pythonhosted.org/packages/f3/18/'
    '6d4e1274f221073058b621f4df8050958b7564b24b4fa25be9f1b7639274/'
    'numpy-2.2.0-pp310-pypy310_pp73-macosx_10_15_x86_64.whl'
)

main(url_numpy_win32)
main(url_numpy_macos)

# numpy-2.2.0-cp313-cp313t-win32.whl
# File size: 6325288 bytes
# Downloaded metadata: 69107 bytes

# numpy-2.2.0-pp310-pypy310_pp73-macosx_10_15_x86_64.whl
# File size: 21043901 bytes
# Downloaded metadata: 85108 bytes
```

The archive files were 6.3 MB and 21 MB in size, and we only had to download ~100 KB of metadata to list the files. It is technically possible to download even smaller part of the zip files, but I didn't think it was worth the effort. Apparently, it may be rather tricky to be able to locate certain sections of metadata within a zip file because sections can vary in size and order depending on the options that were used when the zip file was created (e.g. compression, optional metadata, and encryption). The Internet is full of stories where due to variable-length fields used for filenames, extra fields, and comments folks struggled to predict where one piece of metadata ends and another begins without carefully parsing each section.

Knowing the filename, it is also possible to locate the files in the archive (in terms of the byte range) and to download only a single file out of the archive, however, this felt a bit unnecessary for my personal use case (but of course would be encouraged to implement in a professional setting).
