import pytest
import pandas as pd
import os


# Test that results.csv is not empty
def test_file_content():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    assert df.shape[0] > 0, f"No data in {path} "


def test_duplicate():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    duplicate = df.drop_duplicates(subset=['ISO', 'Variable', 'Aggregation', 'Year']).shape[0] - df.shape[0]
    assert duplicate == 0, f"Duplicated values in {path}"


def test_missing_values():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    n_missing = abs(df.dropna(subset=['ISO', 'Year', 'Variable','Aggregation']).shape[0] - df.shape[0])
    assert n_missing == 0, f"{n_missing} Missing values in {path}"



def test_Variables():
    df = pd.read_csv('data/full_data/result.csv')
    Variables = [file for file in os.listdir('data/indicator/') if (len(file)==3 and file != 'TMP')] + ['ESRU', 'SI', 'GEO', 'NCP', 'Index']
    Variables_in_df = df.Variable.unique()
    assert set(Variables) <= set(Variables_in_df), f'Variables are missing'

def test_columns():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    assert set(['ISO', 'Year', 'Variable','Aggregation', 'Value','Continent','UNregion','IncomeLevel']) <= set(df.columns), f"Columns are missing in {path}"


def test_file_presence():
    path = f'data/full_data'
    files = os.listdir(path)
    assert len(files) > 0, f"No files in {path}"
