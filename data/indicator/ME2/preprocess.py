import pandas as pd


def process_ME2():
    df = (
        pd.read_csv('data/indicator/ME2/raw/ME2_UNEP.M.csv')
          .melt(id_vars=['Country', 'Flow Type'], var_name='Year', value_name='Value')
          .rename(columns={"Flow Type": 'Description'}) 
          .dropna()
    )
    return df
