import pandas as pd


def process_GJ1():

    df = pd.read_excel('data/indicator/GJ1/raw/GJ1_GGGI.M.xlsx')
    df = df.rename(columns={'GEMPsh': 'Value', 'cname': 'Country', 'year': 'Year'})
    df = df.drop(columns=['country'])
    return df
