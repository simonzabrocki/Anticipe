import pytest
import os

indicators = [file for file in os.listdir('data/indicator/') if len(file)==3]


@pytest.mark.parametrize(('indicator'), indicators)
def test_raw_files_presence(indicator):
    files = os.listdir(f'data/indicator/{indicator}/raw')
    assert len(files) > 0, f"No files in {indicator}/raw"
