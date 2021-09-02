import pandas as pd

def preprocess():
    
    df = (
        pd.read_csv('data/indicator/GN2/raw/GN2_IRENA.M.csv', header=5)
          .rename(columns={'RE or Non-RE': 'Type', 'ISO Code': 'ISO'})
          .query('Type == "Total Renewable"')
    )
    
    df['Value'] = df['Electricity Installed Capacity (MW)'].replace(',','', regex=True).astype(float)
    df['Year'] = df['Year'].astype(int)
    df = df.groupby(['ISO', 'Year'])['Value'].sum().reset_index()
    
    pop = (
        pd.read_csv('data/indicator/GN2/raw/GN2.0_WB.M.csv')
          .drop(columns=['Country Name', 'Indicator Code', 'Indicator Name'])
          .rename(columns={'Country Code': 'ISO'})
          .melt(id_vars=['ISO'], var_name='Year', value_name='Value')
    )
    pop['Year'] = pop['Year'].astype(int)

    df = pd.merge(df, pop, on=['ISO', 'Year'], suffixes=('_capa', '_pop'))
    
    df['Value'] = df['Value_capa'] / df['Value_pop'] * 1e6
    return df[['ISO', 'Year', 'Value']]


config = {'Variable': 'GN2',
           'function': preprocess,
           'Description': 'Installed renewable electricity-generating capacity (watts per capita)',
           'Source': 'IRENA and world bank',
           'URL': 'https://www.irena.org/Statistics/View-Data-by-Topic/Renewable-Energy-Balances/Country-Profiles'}