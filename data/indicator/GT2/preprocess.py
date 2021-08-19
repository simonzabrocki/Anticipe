import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/GT2/raw/GT2_FAO.M.csv')
          .pivot(index=['Area', 'Year'], columns=['Element'], values='Value')
    )
    
    df['Value'] = (df['Export Quantity'] / df['Food'])
    return df['Value'].reset_index().rename(columns={'Area': 'Country'})


config =  {'Variable': 'GT2',
            'function': preprocess,
            'Description': 'Share of fish exports to domestic consumption',
            'Source': 'FAO',
            'URL': 'http://www.fao.org/faostat/en/#data/FBS'
            }