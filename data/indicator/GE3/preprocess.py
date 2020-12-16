import pandas as pd


def process_GE3_1(df):
    res = pd.DataFrame()
    res = df.groupby(['ISO', 'Year', 'sector', 'Country', 'Source'])['Value'].sum().reset_index()
    Agri = res[res.sector == 'Agriculture'].set_index(['ISO', 'Year', 'Country', 'Source']).drop(columns='sector')
    LUCF = res[res.sector == 'Land-Use Change and Forestry'].set_index(['ISO', 'Year', 'Country', 'Source']).drop(columns='sector')
    res = (LUCF + Agri).reset_index()
    description = ' '.join(df.gas.unique()) + ' ' + ' and '.join(df.sector.unique()) + ' Tons' # ' MtCO2eq' #
    res['Description'] = description
    res['Value'] = res['Value'] *  1e6
    return res
