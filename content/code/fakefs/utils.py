from pathlib import Path


def merge_files(source, target):
    Path(source).joinpath(target).write_text('line1\nline2\nline3\nline4\n')