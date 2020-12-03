import pandas as pd

from data.indicator.GE3.process import GE3_computation_config
from data.indicator.GE2.process import GE2_computation_config
from data.indicator.GE1.process import GE1_computation_config
from data.indicator.GB2.process import GB2_WB_computation_config, GB2_SDG_computation_config
from data.indicator.BE1.process import BE1_computation_config
from data.indicator.SE2.process import SE2_WB_computation_config, SE2_SDG_computation_config
from data.indicator.SE1.process import SE1_computation_config
from data.indicator.AB3.process import AB3_computation_config
from data.indicator.AB2.process import AB2_SDG_computation_config, AB2_WB_computation_config
from data.indicator.AB1.process import AB1_SDG_computation_config, AB1_WB_computation_config


indicators_computations = {
    'GE3': [('GE3.csv', GE3_computation_config)],
    'GE2': [('GE2.csv', GE2_computation_config)],
    'GE1': [('GE1.csv', GE1_computation_config)],
    'GB2': [('GB2_WB.csv', GB2_WB_computation_config), ('GB2_SDG.csv', GB2_SDG_computation_config)],
    'BE1': [('BE1.csv', BE1_computation_config)],
    'SE2': [('SE2_WB.csv', SE2_WB_computation_config), ('SE2_SDG.csv', SE2_SDG_computation_config)],
    'SE1': [('SE1.csv', SE1_computation_config)],
    'AB3': [('AB3.csv', AB3_computation_config)],
    'AB2': [('AB2_SDG.csv', AB2_SDG_computation_config), ('AB2_WB.csv', AB2_WB_computation_config)],
    'AB1': [('AB1_SDG.csv', AB1_SDG_computation_config), ('AB1_WB.csv', AB1_WB_computation_config)],
}


def compute_from_df(df, config):
    var = config['sub_variables']
    From = config['From']
    function = config['function']
    Description = config['Description'](var)
    Variable = config['Variable']

    df = df[df.Description.isin(var) & (df.From.isin(From))].drop_duplicates(subset=['ISO', 'Year', 'Description', 'From', 'Value'])

    pivot = df.pivot(index=['ISO', 'Year'], columns='Description', values='Value')

    result = pd.DataFrame()
    result['Value'] = function(pivot, var)
    result['Description'] = Description
    result['Variable'] = Variable
    result['From'] = ' _AND_ '.join(From)
    result['Source'] = ' _AND_ '.join(df['Source'].unique())
    result['URL'] = ' _AND_ '.join(df['URL'].unique())

    return result.reset_index().dropna(subset=['Value'])


def compute_from_path(config, path):
    files = config['files']
    df = pd.concat([pd.read_csv(f'{path}/{file}') for file in files])
    return compute_from_df(df, config)
