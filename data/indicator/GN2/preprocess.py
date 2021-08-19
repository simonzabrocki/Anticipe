import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def preprocess():
    df_1 = pd.read_csv('data/indicator/GN2/raw/PM25_mean_exposure.M.csv').dropna(axis=1).rename(columns={'Value': 'PM25_mean_exposure'})
    df_2 = pd.read_csv('data/indicator/GN2/raw/transport_GHG.M.csv').dropna(axis=1).rename(columns={'Value': 'transport_GHG'})

    
    df = pd.concat([df_1.set_index(['Country']), df_2.set_index(['Country'])], axis=1).drop(columns=['Year']).dropna()

    df['PM25_mean_exposure'] *= -1
    df['transport_GHG'] *= -1

    df_norm = pd.DataFrame(MinMaxScaler(feature_range=(1, 100)).fit_transform(df), columns=df.columns, index=df.index)
    return df_norm.mean(axis=1).to_frame(name='Value').assign(Year=2020).reset_index()


config =  {'Variable': 'GN2',
              'function': preprocess,
              'Description': 'Green Mobility in sustainable transport',
              'Source': 'sum4all',
              'URL': 'https://www.sum4all.org/gra-tool/country-performance/global'}