import pandas as pd


def preprocess():

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


config = {'Variable': 'GB3',
          'function': preprocess,
          'Description': 'Getting paid, laws and regulations for equal gender pay score',
          'Source': 'World Bank Women, Business and the Law',
          'URL': 'http://wbl.worldbank.org/en/reports'}