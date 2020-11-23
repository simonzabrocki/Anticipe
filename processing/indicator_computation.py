import pandas as pd


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
