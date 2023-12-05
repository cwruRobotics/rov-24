"""Test mypy on this module."""
import os

import pytest
from ament_mypy.main import main


@pytest.mark.mypy
@pytest.mark.linter
def test_mypy() -> None:
    """Tests mypy on this module."""
    file_path = __file__.replace(f'{__name__}.py', '')
    config_file = os.path.join(file_path, '..', '..', '..', '..', 'mypy.ini')
    error_code = main(argv=['--config', config_file])
    assert error_code == 0, 'Found code style errors / warnings'
