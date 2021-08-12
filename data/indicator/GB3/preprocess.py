import pandas as pd


def process_GB3():

    df = (
        pd.ExcelFile('data/indicator/GB3/raw/GB3_WB.M.xlsx')
          .parse('1971-2021')
    )
    
    df = df[['economy', 'wbcodev2', 'reportyr', 'PAY']]

    df = df.rename(
         columns={
             'economy': 'Country',
             'wbcodev2': 'ISO',
             'reportyr': 'Year',
             'PAY': 'Value'
         })
    return df


config_GB3 = {'Variable': 'GB3',
          'function': process_GB3,
          'Description': 'Getting paid, laws and regulations for equal gender pay score',
          'Source': 'World Bank Women, Business and the Law',
          'URL': 'http://wbl.worldbank.org/en/reports'}