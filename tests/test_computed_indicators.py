import pytest
import os
import pandas as pd

#indicators = ['GE3', 'GE2', 'GE1', 'GB2', 'BE1', 'SE2', 'SE1', 'AB3', 'AB2', 'AB1']
indicators = ['GE3', 'GE2', 'GE1', 'GB2', 'BE1', 'SE2', 'SE1', 'AB1']


def get_computed_files_from_indicator(indicator):
    files = os.listdir(f'data/indicator/{indicator}/computed')

    return [(file, indicator) for file in files]


def get_computed_files(indicators):
    files = [get_computed_files_from_indicator(indicator) for indicator in indicators]
    files = [item for sublist in files for item in sublist]
    return files


computed_files = get_computed_files(indicators)


@pytest.mark.parametrize(('indicator'), indicators)
def test_prepocessed_files_presence(indicator):
    files = get_computed_files_from_indicator(indicator)
    assert len(files) > 0, f"No files in {indicator}/computed"


@pytest.mark.parametrize(('computed_files'), computed_files)
def test_prepocessed_df_content(computed_files):
    file, indicator = computed_files
    path = f'data/indicator/{indicator}/computed/{file}'
    df = pd.read_csv(path)
    assert df.shape[0] > 0, f"No data in {path} "


@pytest.mark.parametrize(('computed_files'), computed_files)
def test_prepocessed_df_columns(computed_files):
    file, indicator = computed_files
    path = f'data/indicator/{indicator}/computed/{file}'
    df = pd.read_csv(path)
    assert set(['ISO', 'Year', 'Value', 'Variable', 'Source', 'URL', 'From']) <= set(df.columns), f"Columns are missing in {path}"


@pytest.mark.parametrize(('computed_files'), computed_files)
def test_prepocessed_df_missing_values(computed_files):
    file, indicator = computed_files
    path = f'data/indicator/{indicator}/computed/{file}'
    df = pd.read_csv(path)
    missing_values = df.dropna(subset=['ISO', 'Year', 'Value', 'Variable']).shape[0] - df.shape[0]
    assert missing_values == 0, f"Missing values in {path}"


@pytest.mark.parametrize(('computed_files'), computed_files)
def test_prepocessed_df_duplicates(computed_files):
    file, indicator = computed_files
    path = f'data/indicator/{indicator}/computed/{file}'
    df = pd.read_csv(path)
    duplicates = df.drop_duplicates(subset=['ISO', 'Variable', 'Year']).shape[0] - df.shape[0]
    assert duplicates == 0, f"Duplicated values in {path}"
