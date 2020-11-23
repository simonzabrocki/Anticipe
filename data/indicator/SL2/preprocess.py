import pandas as pd


def process_SL2():

    df = pd.read_csv('data/indicator/SL2/raw/SL2_GGGI.M.csv')
    return df[['ISO', 'Year', 'Value']]
