import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/SL2/raw/SL2_FAO.M.csv')[['Year', 'Area', 'Item', 'Value']]
          
    )
    agri_orga = df.query('Item == "Agriculture area under organic agric."').set_index(["Year", 'Area'])[['Value']]
    agri_tot = df.query('Item == "Agricultural land"').set_index(['Year', 'Area'])[['Value']]
    
    df = (agri_orga / agri_tot * 100).reset_index().dropna().rename(columns={'Area': 'Country'})
    
    
    return df


config =  {'Variable': 'SL2',
               'function': preprocess,
               'Description': 'Share agriculture organic to total agriculture land area (Percent)',
               'Source': 'FAOSTAT',
               'URL': 'http://www.fao.org/faostat/en/#data/EL'}