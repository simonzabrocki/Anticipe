import pandas as pd


def process_SL1():

    df = pd.read_csv('data/indicator/SL1/raw/SL1_GGGI.M.csv', index_col=0)
    df = df.rename(columns={'SL1_GGGI': 'Value'})

    return df
