import pandas as pd
import country_converter as coco
import logging
logging.disable(logging.WARNING)


def add_ISO(df):
    df = df.copy()

    def filter_ISO(ISO):
        if type(ISO) == list or len(ISO) != 3:
            return None
        else:
            return ISO

    Countries = df['Country'].unique()
    cc = coco.CountryConverter()
    ISOs = cc.convert(Countries.tolist(), to='ISO3', not_found=None)
    ISOs = list(map(filter_ISO, ISOs))
    keys = pd.DataFrame([Countries, ISOs]).T.rename(columns={
        0: 'Country',
        1: 'ISO'
    })

    df = pd.merge(keys, df, on='Country')
    return df.dropna(subset=['ISO'])
