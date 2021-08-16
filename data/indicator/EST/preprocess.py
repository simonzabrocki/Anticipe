import pandas as pd


def process_EST():
    df=pd.read_excel('data/indicator/EST/raw/EST_SUM4ALL.M.xlsx')
    df = df.drop(columns=['Delta', 'Time Series'])
    df=df.dropna()
    return df

config_EST ={'Variable': 'EST',
             'function': process_EST,
             'Description': 'Efficiency in sustainable transport',
             'Source': 'sum4all',
             'URL': 'https://www.sum4all.org/gra-tool/country-performance/indicators'}
