import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess():
    df_1 = pd.read_csv('data/indicator/GS3/raw/Rural access index.csv').dropna(axis=1).rename(columns={'Value': 'Rural access index'})
    df_2 = pd.read_csv('data/indicator/GS3/raw/Percentage of female workers in transport.csv').dropna(axis=1).rename(columns={'Value': 'Percentage female workers in transport'})
    df_3 = pd.read_csv('data/indicator/GS3/raw/Rapid Transit to Resident Ratio.csv').dropna(axis=1).rename(columns={'Value': 'Rapid Transit to Resident Ratio'})

    
    df = pd.concat([df_1.set_index(['Country']), df_2.set_index(['Country']), df_3.set_index(['Country'])], axis=1).drop(columns=['Year']).dropna()

    
    df_norm = pd.DataFrame(MinMaxScaler(feature_range=(1, 100)).fit_transform(df), columns=df.columns, index=df.index)
    return df_norm.mean(axis=1).to_frame(name='Value').assign(Year=2020).reset_index()


config =  {'Variable': 'AB3',
              'function': preprocess,
              'Description': 'Universal access - sustainable transport',
              'Source': 'sum4all',
              'URL': 'https://www.sum4all.org/gra-tool/country-performance/global'}