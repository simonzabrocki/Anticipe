import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# def preprocess():
#     df = (
#         pd.read_csv('data/indicator/EE3/raw/logistics_index.M.csv')
#           .dropna(axis=1).rename(columns={'Value': 'Logistic index'})
#           .set_index('Country')
#     )

#     df_norm = pd.DataFrame(MinMaxScaler(feature_range=(1, 100)).fit_transform(df), columns=df.columns, index=df.index)
#     return df_norm.mean(axis=1).to_frame(name='Value').assign(Year=2020).reset_index()


def preprocess():
    data = pd.read_excel("data/indicator/EE3/raw/LPI_from_2007_to_2018.M.xlsx", skiprows=2 , sheet_name=[0,1,2,3,4,5])
    year_list = [2018, 2016, 2014, 2012, 2010, 2007]
    
    
    df = (
        pd.concat([df.assign(Year=year_list[i]) for i, df in data.items()], axis=0)
          .rename(columns = {'Code':'ISO', 'score': 'Value'})
          .set_index(['ISO', 'Year'])['Value']
          .dropna()

    )
    return df.reset_index()

config =  {'Variable': 'EE3',
              'function': preprocess,
              'Description': 'logistics performance index (LPI) of the World Bank',
              'Source': 'Wolrd Bank',
              'URL': 'https://lpi.worldbank.org/ '}