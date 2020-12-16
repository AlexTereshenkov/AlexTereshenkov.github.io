from datetime import datetime
from unittest.mock import patch, Mock
from client import Client

def setattrs(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)


def test_process():
    mock_client = Mock()
    with patch('client.Client', lambda: mock_client):
        mock_client.process.side_effect = lambda: setattrs(mock_client,
            visited=True, last_time_visited=datetime.now())
        client = Client(99)
        client.process()
        assert client.visited is True
        assert isinstance(client.last_time_visited, datetime)
        