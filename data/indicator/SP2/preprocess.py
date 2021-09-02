import pandas as pd


def preprocess():
    df = pd.read_csv('data/indicator/SP2/raw/SP2_GHD.M.csv')

    df = df[df['indicator_name'] == 'Healthcare Access and Quality'][[
        'location_name', 'year_id', 'val']]

    df = df.rename(columns={'location_name': 'Country', 'year_id': 'Year', 'val': 'Value'})

    return df


config = {'Variable': 'SP2',
          'function': preprocess,
          'Description': 'Health care Access and Quality Index',
          'Source': 'Institute for Health Metrics and Evaluation, based on Global Burden of Disease Study 2015 (GBD 2015).',
          'URL': 'http://ghdx.healthdata.org/record/global-burden-disease-study-2015-gbd-2015-healthcare-access-and-quality-index-based-amenable'}