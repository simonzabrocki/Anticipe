import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/ME3/raw/ME3.2_FAO.M.csv')
          .groupby(['Area', 'Year', 'Element'])['Value'].sum().reset_index()
          .pivot(index=['Area', 'Year'], columns='Element', values='Value')
    )
    
    df['Value'] = df['Loss'] / df['Production'] * 100
    return df['Value'].reset_index().rename(columns={'Area': 'Country'})



config =  {'Variable': 'ME3.2',
              'function': preprocess,
              'Description': 'Share food loss to total food production (Percent)',
              'Source': 'FAO',
              'URL': 'http://www.fao.org/faostat/en/#data/SCL'
              }