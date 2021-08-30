import pytest
import pandas as pd
import os


# Test that results.csv is not empty
def test_file_content():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    assert df.shape[0] > 0, f"No data in {path} "

    # Test that there is not duplicates
def test_duplicate():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    duplicate = df.drop_duplicates(subset=['ISO', 'Variable', 'Year']).shape[0] - df.shape[0]
    assert duplicate == 0, f"Duplicated values in {path}"
    
# Test that there is not NaN
def test_missing_values():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    NaN = df.dropna(subset=['ISO', 'Year', 'Value', 'Variable','Aggregation']).shape[0] - df.shape[0]
    assert NaN == 0, f"Missing values in {path}"
    
# Test that there is all indicator include
Variables = [file for file in os.listdir('data/indicator/') if (len(file)==3 and file != 'TMP')]
def test_Variables():
    df = pd.read_csv('data/full_data/result.csv')
    Variables_in_df = df.Variable.unique()
    assert set(Variables_in_df) == set(Variables)

#Test columns
def test_columns():
    path = f'data/full_data/result.csv'
    df = pd.read_csv(path)
    assert set(['ISO', 'Year', 'Variable','Aggregation', 'Value','Continent','UNregion','IncomeLevel']) <= set(df.columns), f"Columns are missing in {path}"


#Test file presence 

def test_file_presence():
    path = f'data/full_data'
    file = get_result_file_from_full_data(path)
    assert len(files) > 0, f"No files in {path}"

    


