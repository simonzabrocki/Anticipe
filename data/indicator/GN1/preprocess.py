import pandas as pd
from processing.utils import add_ISO

def process_GN1():
    df = (
        pd.read_csv('data/indicator/GN1/raw/GN1_WIPO.M.csv')
          .drop(columns=['Origin', 'Office (Code)']).rename(columns={'Office': 'Country'})
          .melt(id_vars=['Country', 'Field of technology'], var_name='Year', value_name='Value')
    )
    
    df = add_ISO(df)
    
    env = df[df['Field of technology'] == '24 - Environmental technology'].drop(columns=['Field of technology']).set_index(['Country', 'ISO', 'Year'])
    total = df.groupby(['Country', 'ISO', 'Year']).sum()
    
    df = (env / total).reset_index()
    df['Value'] = df.groupby(['ISO'])['Value'].transform(lambda x: x.rolling(7, 1).mean())

    return df



config_GN1 = {'Variable': 'GN1',
           'function': process_GN1,
           'Description': 'Cumulative Share of patent publications in environmental technology to total patents',
           'Source': 'World Intellectual Property Organization (WIPO) statistics database',
           'URL': 'https://www3.wipo.int/ipstats/index.htm?tab=patent'}