import pandas as pd


def process_ME2():
    df = pd.read_csv('data/indicator/ME2/raw/ME2_GGGI.M.csv', index_col=0)
    return df
