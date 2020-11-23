import pandas as pd


def process_SP2():
    df = pd.read_csv('data/indicator/SP2/raw/SP2_GHD.M.csv')

    df = df[df['indicator_name'] == 'Healthcare Access and Quality'][[
        'location_name', 'year_id', 'val']]

    df = df.rename(columns={'location_name': 'Country', 'year_id': 'Year', 'val': 'Value'})

    return df
