import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/ME2/raw/ME2_UNEP.M.csv')
          .melt(id_vars=['Country', 'Flow Type'], var_name='Year', value_name='Value')
          .rename(columns={"Flow Type": 'Description'}) 
          .dropna()
    )
    return df


config = {'Variable': 'ME2',
              'function': preprocess,
              'Description': 'Total material footprint (MF) per capita',
              'Source': 'U.N. Environment: Secretariat of the International Resource Panel',
              'URL': 'https://www.resourcepanel.org/global-material-flows-database'
             }
