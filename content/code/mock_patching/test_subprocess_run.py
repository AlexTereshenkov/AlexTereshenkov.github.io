import subprocess
import pytest
from unittest.mock import patch, Mock
from subprocess import CalledProcessError
from subprocess_run import call_cmd


def test_call_cmd():
    run_mock = Mock()
    run_mock.check_returncode.return_value = "0"
    with patch('subprocess_run.subprocess.run', lambda cmd: run_mock):
        assert call_cmd('du -sh lib') == "0"
    
    run_mock = Mock()
    run_mock.check_returncode.side_effect = subprocess.CalledProcessError(0,0)
    with patch('subprocess_run.subprocess.run', lambda cmd: run_mock):        
        with pytest.raises(CalledProcessError):
            call_cmd('du -sh non-existing-dir')
