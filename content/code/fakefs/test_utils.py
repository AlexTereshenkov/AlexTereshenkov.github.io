from pathlib import Path

from pyfakefs.pytest_plugin import Patcher as FakeFileSystem
from utils import merge_files


def test_merge_files():
    with FakeFileSystem() as _:
        dest_dir = Path('/opt/data')
        dest_dir.mkdir(parents=True)
        dest_dir.joinpath('file1').write_text('line1\nline2\n')
        dest_dir.joinpath('file2').write_text('line3\nline4\n')

        merge_files(source=dest_dir, target='result')
        assert dest_dir.joinpath(
            'result').read_text() == 'line1\nline2\nline3\nline4\n'
