from unittest.mock import patch, Mock
import pytest

from db import get_table, delete_db_table, delete_table


@patch('db.delete_table', lambda name: True)
def test_delete_db_table():
    get_table_mock = Mock()

    # db table gets deleted
    get_table_mock.side_effect = [True, False]
    with patch('db.get_table', get_table_mock):
        assert delete_db_table("LogHistory")

    # db table fails to be deleted
    get_table_mock.side_effect = [True, True]
    with patch('db.get_table', get_table_mock):
        with pytest.raises(ValueError):
            delete_db_table("LogHistory")
