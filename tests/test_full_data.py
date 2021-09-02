import pytest
import pandas as pd
import os

indicators = [file for file in os.listdir('data/indicator/') if (len(file)==3 and file != 'TMP')]

def test_indicators():
    df = pd.read_csv('data/full_data/data.csv')
    indicators_in_df = df.Indicator.unique()
    assert set(indicators_in_df) == set(indicators)


def test_columns():
    df = pd.read_csv('data/full_data/data.csv')
    columns = df.columns
    assert set(columns) >= set(['ISO', 'Year', 'Indicator', 'Source', 'Imputed', 'Value'])
