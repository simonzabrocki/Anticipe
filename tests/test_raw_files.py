import pytest
import os


indicators = ['GV1', 'EE2', 'SE2', 'CV2', 'ME1', 'BE3', 'ME2',
              'BE2', 'SP1', 'EW1', 'EQ1', 'CV3', 'SE1', 'CV1',
              'GT1', 'SP3', 'SE3', 'GB3', 'GE1', 'GB2', 'GJ1',
              'SP2', 'EW2', 'EE1', 'SL1', 'AB3', 'AB2', 'EQ2',
              'AB1', 'SL2', 'EQ3', 'GB1', 'BE1', 'GE3', 'GE2', 'GN1']


@pytest.mark.parametrize(('indicator'), indicators)
def test_raw_files_presence(indicator):
    files = os.listdir(f'data/indicator/{indicator}/raw')
    assert len(files) > 0, f"No files in {indicator}/raw"
