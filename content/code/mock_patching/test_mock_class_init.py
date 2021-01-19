from unittest.mock import patch
from pathlib import Path
from typing import List
from enum import auto, Enum


class ProcessorConfiguration:
    pass


class ValidationStatus(Enum):
    SUCCESS = 1
    FAILURE = 1


class FileProcessor:
    def __init__(self, files: List[Path], process_config: ProcessorConfiguration):
        self.files = files
        self.process_config = process_config

    def validate_files(self):
        # operate on the files and return some validation result
        ...
        return {"status": ValidationStatus.SUCCESS}


def test_validate_files():
    with patch.object(FileProcessor, '__init__', lambda self: None):
        fp = FileProcessor()
        fp.files = [Path('foo'), Path('bar')]
        assert fp.validate_files().get("status") == ValidationStatus.SUCCESS

        fp.files = []
        assert fp.validate_files().get("status") == ValidationStatus.FAILURE
