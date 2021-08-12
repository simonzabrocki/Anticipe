import pandas as pd


def process_CV2():

    df = pd.read_csv('data/indicator/CV2/raw/CV2_OCEANHEALTHINDEX.M.csv')
    df = df[(df['goal'] == 'TR') & (df.dimension == 'score')]
    df = df[['scenario', 'value', 'region_name']]
    df = df.rename(columns={
        'scenario': 'Year',
        'value': 'Value',
        'region_name': 'Country'
    })

    return df

config_CV2 =  {'Variable': 'CV2',
          'function': process_CV2,
          'Description': 'Tourism and recreation in coastal and marine areas score',
          'Source': 'Ocean Health Index',
          'URL': 'http://ohi-science.org/ohi-global/download'}