import pandas as pd


def process_GB3():

    xls = pd.ExcelFile('data/indicator/GB3/raw/GB3_WB.M.xlsx')

    dfs = {
        sheet_name: xls.parse(sheet_name, header=1)
        for sheet_name in xls.sheet_names
    }

    df = dfs['WBL1971-2020'][[
        'Economy', 'Code', 'WBL Report Year', 'PAY'
    ]]

    df = df.rename(
        columns={
            'Economy': 'Country',
            'Code': 'ISO',
            'WBL Report Year': 'Year',
            'PAY': 'Value'
        })

    return df
