from unittest.mock import patch
from static_class import Address, is_valid_address


def test_is_valid_address():
    with patch('static_class.Address.from_tuple', lambda *data: True):
        assert is_valid_address(("1", "New Road", "99999", "City"))

    with patch('static_class.Address.from_tuple', side_effect=Exception()):
        assert not is_valid_address(("1", "New Road", "99999", "City"))


def test_address_construct():
    with patch('static_class.Address.numerize', lambda value: 9999):
        address = Address(*("1", "New Road", "99999", "City"))
        assert address.city == "City"
        assert address.house == 9999


def test_print():
    with patch('static_class.Address.to_string', lambda value: "Address formatted"):
        address = Address(*("1", "New Road", "99999", "City"))
        assert address.print() == "Address formatted"
