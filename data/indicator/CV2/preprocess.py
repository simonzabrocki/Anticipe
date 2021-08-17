import pandas as pd


def preprocess():

    df = pd.read_csv('data/indicator/CV2/raw/CV2_OCEANHEALTHINDEX.M.csv')
    df = df[(df['goal'] == 'TR') & (df.dimension == 'score')]
    df = df[['scenario', 'value', 'region_name']]
    df = df.rename(columns={
        'scenario': 'Year',
        'value': 'Value',
        'region_name': 'Country'
    })

    return df

config =  {'Variable': 'CV2',
              'function': preprocess,
              'Description': 'Tourism and recreation in coastal and marine areas score',
              'Source': 'Ocean Health Index',
              'URL': 'http://ohi-science.org/ohi-global/download'}