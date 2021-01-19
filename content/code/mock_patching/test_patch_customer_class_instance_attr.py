from typing import List
from unittest.mock import patch, MagicMock


def test_customer_address():
    with patch('customer.Customer') as mock_customer:
        c = mock_customer.return_value
        mock_address = MagicMock()
        # MagicMock lets you define nested attributes
        mock_address.city.name = "BigCity"
        c.get_address.return_value = mock_address
        assert c.get_address().city.name == 'BigCity'
