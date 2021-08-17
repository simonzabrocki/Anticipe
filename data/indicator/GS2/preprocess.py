import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/TMP/raw/TMP_IEA.M.csv')
          .melt(id_vars=['Country', 'Mode/vehicle type', 'Indicator'], var_name=['Year'], value_name='Value')
          .rename(columns={'Mode/vehicle type': 'mode'})
          .assign(Indicator=lambda x: x.Indicator.str.strip())
          .query("mode == 'Total passenger transport' and Indicator == 'Passenger-kilometres energy intensity (MJ/pkm)'")
          .drop(columns=['mode', 'Indicator'])
          .dropna()
    )
    return df
    
config = {'Variable': 'GS1',
             'function': preprocess,
             'Description': 'Total passenger transport Passenger-kilometres energy intensity (MJ/pkm)',
             'Source': 'IEA',
             'URL': 'https://www.iea.org/data-and-statistics/data-product/energy-efficiency-indicators'}