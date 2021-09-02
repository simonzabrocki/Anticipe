import pytest
import os
import pandas as pd


indicators = [file for file in os.listdir('data/indicator/') if len(file)==3 and file != 'TMP'] 

def get_preprocessed_files_from_indicator(indicator):
    files = os.listdir(f'data/indicator/{indicator}/preprocessed')
    return [(file, indicator) for file in files]


def get_preprocessed_files(indicators):
    files = [get_preprocessed_files_from_indicator(indicator) for indicator in indicators]
    files = [item for sublist in files for item in sublist]
    return files


preprocessed_files = get_preprocessed_files(indicators)


@pytest.mark.parametrize(('indicator'), indicators)
def test_prepocessed_files_presence(indicator):
    files = get_preprocessed_files_from_indicator(indicator)
    assert len(files) > 0, f"No files in {indicator}/preprocessed"


@pytest.mark.parametrize(('preprocessed_file'), preprocessed_files)
def test_prepocessed_df_content(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/preprocessed/{file}'
    df = pd.read_csv(path)
    assert df.shape[0] > 0, f"No data in {path} "


@pytest.mark.parametrize(('preprocessed_file'), preprocessed_files)
def test_prepocessed_df_columns(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/preprocessed/{file}'
    df = pd.read_csv(path)
    assert set(['ISO', 'Year', 'Value', 'Variable', 'Source', 'URL', 'From']) <= set(df.columns), f"Columns are missing in {path}"


@pytest.mark.parametrize(('preprocessed_file'), preprocessed_files)
def test_prepocessed_df_missing_values(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/preprocessed/{file}'
    df = pd.read_csv(path)
    missing_values = df.dropna(subset=['ISO', 'Year', 'Value', 'Variable']).shape[0] - df.shape[0]
    assert missing_values == 0, f"Missing values in {path}"


@pytest.mark.parametrize(('preprocessed_file'), preprocessed_files)
def test_prepocessed_df_duplicates(preprocessed_file):
    file, indicator = preprocessed_file
    path = f'data/indicator/{indicator}/preprocessed/{file}'
    df = pd.read_csv(path)
    duplicates = df.drop_duplicates(subset=['ISO', 'Variable', 'Year']).shape[0] - df.shape[0]
    assert duplicates == 0, f"Duplicated values in {path}"
