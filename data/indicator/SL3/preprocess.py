import pandas as pd


def preprocess():
    df = (
        pd.read_csv('data/indicator/SL3/raw/SL3_FAO.M.csv')
          .groupby(['Area', 'Year'])['Value'].sum().reset_index()
          .rename(columns={'Area': 'Country', 'value': 'Value', 'year': 'Year'})
    )
    return df



config =  {'Variable': 'SL3',
              'function': preprocess,
              'Description': 'Livestock units per agricultural land area (LSU/ha)',
              'Source': 'FAO',
              'URL': 'http://www.fao.org/faostat/en/?fbclid=IwAR0dEJjoD4nMZkIqQehBdP04CfE2noGLbSUl7CHh_VfRbn4ugcAqEgAWgSc#data/EK'}