import pandas as pd


def process_ME1():
    df = pd.read_csv("data/indicator/ME1/raw/ME1_OECD.M.csv")
    df = df.drop(columns=['INDICATOR', 'SUBJECT', 'MEASURE', 'FREQUENCY','Flag Codes'])
    df.rename(columns={'LOCATION':'ISO', 'TIME':'Year'}, inplace=True)
    
    return df
