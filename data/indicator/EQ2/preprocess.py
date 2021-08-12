import pandas as pd


# def process_EQ2():
#     df = pd.read_csv('data/indicator/EQ2/raw/EQ2_GHD.M.csv')
#     df = df.rename(columns={
#         'location_name': 'Country',
#         'year': 'Year',
#         'val': 'Value'
#     })
#     return df[['Country', 'Year', 'Value']]

def process_EQ2():
    df = (
        pd.read_csv('data/indicator/EQ2/raw/EQ2_GHD.M.csv')
          .query("measure == 'DALYs (Disability-Adjusted Life Years)' and sex == 'Both' and metric == 'Rate'")
          .drop(columns=['sex', 'age', 'cause', 'metric', 'upper', 'lower', 'measure', 'rei'])
          .rename(columns={'location': 'Country', 'year': 'Year', 'val': 'Value'})
    )
    return df


config_EQ2 = {'Variable': 'EQ2',
              'function': process_EQ2,
              'Description': 'DALYs (Disability-Adjusted Life Years), Rate, Age-standardized, Unsafe water source',
              'Source': 'GHD',
              'URL': 'http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2017-permalink/b6989accc192c6a5f121a8204b88f819'}