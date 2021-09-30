from unittest.mock import patch
from class_instance_fields import get_capital


def test_get_capital():
    with patch('class_instance_fields.get_city') as mock:
        mock.return_value.name = "Capital"
        assert get_capital("Country") == "Capital"
