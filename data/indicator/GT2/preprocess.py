import pandas as pd
from processing.utils import add_ISO


def preprocess():
    df = (
        pd.read_csv('data/indicator/GT2/raw/GT2_FAO.M.csv')
          .pivot(index=['Area', 'Year'], columns=['Element'], values='Value')
    )
    df = (
        add_ISO(df.reset_index().rename(columns={"Area": 'Country'}))
        .set_index(['ISO', 'Year'])
         .query('Country != "China, mainland"')
        .drop(columns=['Country'])
    )# ISO must be added to remove regional agregates before computation

    df['Value'] = df['Food'] / df.groupby('Year').Food.sum()
    return df['Value'].dropna().reset_index().rename(columns={'Area': 'Country'})


# def preprocess():
#     df = (
#         pd.read_csv('data/indicator/GT2/raw/GT2_FAO.M.csv')
#           .pivot(index=['Area', 'Year'], columns=['Element'], values='Value')
#     )
    
#     df['Value'] = (df['Export Quantity'] / df['Food'])
#     return df['Value'].reset_index().rename(columns={'Area': 'Country'})


config =  {'Variable': 'GT2',
            'function': preprocess,
            #'Description': 'Share of fish exports to domestic consumption',
            'Description': 'Share of fish exports to total exports',
            'Source': 'FAO',
            'URL': 'http://www.fao.org/faostat/en/#data/FBS'
            }