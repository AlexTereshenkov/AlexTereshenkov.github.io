from unittest.mock import patch

from utils import get_customers


@patch('utils.validate_input', lambda object_type, value: None)
def test_get_customers():
    expected_customers = ['Customer1', 'Customer2']
    with patch('utils.fetch', lambda query: expected_customers):
        actual_customers = get_customers(city='Paris')
        assert actual_customers == expected_customers
