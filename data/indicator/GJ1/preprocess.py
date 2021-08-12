import pandas as pd


def process_GJ1():

    df = pd.read_excel('data/indicator/GJ1/raw/GJ1_GGGI.M.xlsx')
    df = df.rename(columns={'GEMPsh': 'Value', 'cname': 'Country', 'year': 'Year'})
    df = df.drop(columns=['country'])
    return df


config_GJ1 = {'Variable': 'GJ1',
              'function': process_GJ1,
              'Description': 'Share of green manufacturing employment in total manufacturing employment',
              'Source': 'Valentin Todorov',
              'URL': 'Not online'}

