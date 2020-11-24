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


def add_Country_from_ISO(df):
    ISOs = df.ISO.unique()

    ref = coco.CountryConverter().data.set_index('ISO3')
    good_isos = ref.index.intersection(ISOs)

    countries = ref.loc[good_isos]['name_short']
    df = df.set_index('ISO')
    df['Country'] = countries
    return df.dropna(subset=['Country']).reset_index('ISO')
