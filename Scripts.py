import pytest
import pandas as pd
import os


# Test that results.csv is not empty
# Test that there is not duplicates
# Test that there is not na
# Test that there is all indicator include
# ...........

# Test that there is not nan
def test_nan():
    df = pd.read_csv('data/full_data/result.csv')
    df.isnull().values.any()
    
# Test that results.csv is not empty
def test_empty():
    df = pd.read_csv('data/full_data/result.csv')
    isempty = df.empty

# Test that there is not duplicates
def test_duplicate():
    df = pd.read_csv('data/full_data/result.csv')
    duplicate = df[df.duplicated()]


# Test that there is all indicator include
Variables = [file for file in os.listdir('data/indicator/') if (len(file)==3 and file != 'TMP')]
def test_Variables():
    df = pd.read_csv('data/full_data/result.csv')
    Variables_in_df = df.Variable.unique()
   # assert set(Variables_in_df) == set(Variables)


#Test columns
def test_columns():
    df = pd.read_csv('data/full_data/result.csv')
    columns = df.columns
    assert set(columns) >= set(['ISO', 'Year', 'Variable', 'Country', 'Aggregation', 'Value'])


