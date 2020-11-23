import pandas as pd


def process_GE2_0(df):
    res = pd.DataFrame()
    res = df.groupby(['ISO', 'Year', 'sector', 'Country', 'Source'])['Value'].sum().reset_index()
    Agri = res[res.sector == 'Agriculture'].set_index(['ISO', 'Year', 'Country', 'Source']).drop(columns='sector')
    LUCF = res[res.sector == 'Total excluding LUCF'].set_index(['ISO', 'Year', 'Country', 'Source']).drop(columns='sector')
    res = (LUCF - Agri).reset_index()

    description = ' '.join(df.gas.unique()) + ' ' + ' and excluding '.join(df.sector.unique()) + ' Tons'
    res['Value'] = res['Value'] * 1e6
    res['Description'] = description
    return res
