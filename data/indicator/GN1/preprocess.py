import pandas as pd


def process_GN1():

    df = pd.read_csv('data/indicator/GN1/raw/GN1_GGGI.M.csv')
    df['Value'] = df.groupby(['ISO'])['Value'].transform(lambda x: x.rolling(7, 1).mean())
    return df[['ISO', 'Value', 'Year']]
