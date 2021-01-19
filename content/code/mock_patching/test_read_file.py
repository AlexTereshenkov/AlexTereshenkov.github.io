from unittest.mock import patch, mock_open
from read_file import read


def test_read_file():
    with patch('read_file.open', mock_open(read_data="lines")):
        assert read('dir/path') == ["lines"]
