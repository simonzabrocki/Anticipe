import pandas as pd


def preprocess():

    df = pd.read_excel('data/indicator/GJ1/raw/GJ1_GGGI.M.xlsx')
    df = df.rename(columns={'GEMPsh': 'Value', 'cname': 'Country', 'year': 'Year'})
    df = df.drop(columns=['country'])
    return df


config = {'Variable': 'GJ1',
              'function': preprocess,
              'Description': 'Share of green manufacturing employment in total manufacturing employment',
              'Source': 'Valentin Todorov',
              'URL': 'Not online'}

