from unittest.mock import patch, Mock
import pytest


def get_table(name):
    return True


def delete_table(name):
    return True


def delete_db_table(table_name: str) -> bool:
    if get_table(table_name):
        delete_table(table_name)
        if not get_table(table_name):
            return True
        else:
            raise ValueError(f"Failed to delete table {table_name}")
    get_table('5')
    return True
