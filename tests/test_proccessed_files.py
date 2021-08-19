import pytest
import os
import pandas as pd

indicators = [file for file in os.listdir('data/indicator/') if len(file)==3]
# indicators = ['GV1', 'EE2', 'SE2', 'CV2', 'ME1', 'BE3', 'ME2',
#               'BE2', 'SP1', 'EW1', 'EQ1', 'CV3', 'SE1', 'CV1',
#               'GT1', 'SP3', 'SE3', 'GB3', 'GE1', 'GB2', 'GJ1',
#               'SP2', 'EW2', 'EE1', 'SL1', 'AB3', 'AB2', 'EQ2',
#               'AB1', 'SL2', 'EQ3', 'GB1', 'BE1', 'GE3', 'GE2', 'GN1']


def get_processed_files_from_indicator(indicator):
    files = os.listdir(f'data/indicator/{indicator}/processed')
    return [(file, indicator) for file in files]


def get_processed_files(indicators):
    files = [get_processed_files_from_indicator(indicator) for indicator in indicators]
    files = [item for sublist in files for item in sublist]
    return files


processed_files = get_processed_files(indicators)


@pytest.mark.parametrize(('indicator'), indicators)
def test_files_presence(indicator):
    files = get_processed_files_from_indicator(indicator)
    assert len(files) > 0, f"No files in {indicator}/processed"


@pytest.mark.parametrize(('file'), processed_files)
def test_prepocessed_df_content(file):
    file, indicator = file
    path = f'data/indicator/{indicator}/processed/{file}'
    df = pd.read_csv(path)
    assert df.shape[0] > 0, f"No data in {path} "


@pytest.mark.parametrize(('preprocessed_file'), processed_files)
def test_prepocessed_df_columns(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/processed/{file}'
    df = pd.read_csv(path)
    assert set(['ISO', 'Year', 'Value', 'Indicator', 'Source', 'URL', 'From']) <= set(df.columns), f"Columns are missing in {path}"


@pytest.mark.parametrize(('preprocessed_file'), processed_files)
def test_prepocessed_df_duplicates(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/processed/{file}'
    df = pd.read_csv(path)
    duplicates = df.drop_duplicates(subset=['ISO', 'Year']).shape[0] - df.shape[0]
    assert duplicates == 0, f"Duplicated values in {path}"
