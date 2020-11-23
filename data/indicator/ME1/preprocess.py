import pandas as pd


def process_ME1():
    df = pd.read_csv("data/indicator/ME1/raw/ME1_GGGI.M.csv")
    return df
