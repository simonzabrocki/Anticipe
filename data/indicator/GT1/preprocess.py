import pandas as pd


def process_GT1():

    df = pd.read_csv('data/indicator/GT1/raw/GT1_COMTRADE.M.csv', index_col=0, dtype={'cmdCode': str})
    TOTAL = df[df.cmdCode == 'TOTAL']
    ENV_GOODS = df[df.cmdCode != 'TOTAL']

    df = (ENV_GOODS.groupby(['yr', 'rtTitle', 'rt3ISO']).sum(
    ) / TOTAL.set_index(['yr', 'rtTitle', 'rt3ISO']) * 100)['TradeValue'].reset_index()

    df = df.rename(columns={'yr': 'Year',
                            'rtTitle': 'Country',
                            'rt3ISO': 'ISO',
                            'TradeValue': 'Value'})

    return df


config_GT1 = {'Variable': 'GT1',
              'function': process_GT1,
              'Description': 'Share of export of environmental goods (OECD and APEC classifications) to total export (%)',
              'Source': 'UNCOMTRADE data and OECD and APEC classifications of environmental goods',
              'URL': 'https://comtrade.un.org/data/'}