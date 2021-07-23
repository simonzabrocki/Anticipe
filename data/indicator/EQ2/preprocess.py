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