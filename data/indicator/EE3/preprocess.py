import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess():
    df = (
        pd.read_csv('data/indicator/EE3/raw/logistics_index.M.csv')
          .dropna(axis=1).rename(columns={'Value': 'Logistic index'})
          .set_index('Country')
    )

    df_norm = pd.DataFrame(MinMaxScaler(feature_range=(1, 100)).fit_transform(df), columns=df.columns, index=df.index)
    return df_norm.mean(axis=1).to_frame(name='Value').assign(Year=2020).reset_index()


config =  {'Variable': 'EE3',
              'function': preprocess,
              'Description': 'Efficiency in sustainable transport',
              'Source': 'sum4all',
              'URL': 'https://www.sum4all.org/gra-tool/country-performance/global'}