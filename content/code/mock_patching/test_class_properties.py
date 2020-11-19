from unittest.mock import PropertyMock, patch
from class_properties import Process


def test_process_pid_property():
    with patch.object(Process, '__init__', lambda self: None):
        with patch('class_properties.Process.pid', new_callable=PropertyMock) as mock_pid:
            mock_pid.return_value = 99
            process = Process()
            assert process.as_string() == 'Process(99)'
