import pandas as pd


def process_EQ2():
    df = pd.read_csv('data/indicator/EQ2/raw/EQ2_GHD.M.csv')
    df = df.rename(columns={
        'location_name': 'Country',
        'year': 'Year',
        'val': 'Value'
    })
    return df[['Country', 'Year', 'Value']]
