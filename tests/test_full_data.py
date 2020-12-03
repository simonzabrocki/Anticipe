import pytest
import pandas as pd

indicators = ['GV1', 'EE2', 'SE2', 'CV2', 'ME1', 'BE3', 'ME2',
              'BE2', 'SP1', 'EW1', 'EQ1', 'CV3', 'SE1', 'CV1',
              'GT1', 'SP3', 'SE3', 'GB3', 'GE1', 'GB2', 'GJ1',
              'SP2', 'EW2', 'EE1', 'SL1', 'AB3', 'AB2', 'EQ2',
              'AB1', 'SL2', 'EQ3', 'GB1', 'BE1', 'GE3', 'GE2', 'GN1']


def test_indicators():
    df = pd.read_csv('data/full_data/data.csv')
    indicators_in_df = df.Indicator.unique()
    assert set(indicators_in_df) == set(indicators)


def test_columns():
    df = pd.read_csv('data/full_data/data.csv')
    columns = df.columns
    assert set(columns) >= set(['ISO', 'Year', 'Indicator', 'Source', 'Imputed', 'Value'])
