from processing.utils import add_ISO


from data.indicator.CV2.preprocess import config_CV2
from data.indicator.EQ2.preprocess import config_EQ2
from data.indicator.EQ3.preprocess import config_EQ3

from data.indicator.GB3.preprocess import config_GB3
from data.indicator.GJ1.preprocess import config_GJ1
from data.indicator.GN1.preprocess import config_GN1
from data.indicator.GT1.preprocess import config_GT1

from data.indicator.ME1.preprocess import config_ME1
from data.indicator.ME2.preprocess import config_ME2
from data.indicator.SL1.preprocess import config_SL1
from data.indicator.SL2.preprocess import config_SL2
from data.indicator.SP2.preprocess import config_SP2

from data.indicator.TMP.preprocess import config_TMP

# MANUAL 

MANUAL_CONFIGS = {
    'CV2': config_CV2,
    'EQ2': config_EQ2,
    'EQ3': config_EQ3,
    'GJ1': config_GJ1,
    'GN1': config_GN1,
    'GT1': config_GT1,
    'ME1': config_ME1,
    'ME2': config_ME2,
    'SL1': config_SL1,
    'SL2': config_SL2,
    'SP2': config_SP2,
    'TMP': config_TMP,

    
}

exceptions_countries = ['Southern Africa', 'Southern Sub-Saharan Africa',
                        'Micronesia', 'Bassas da India', 'French Guyana',
                        'China, mainland', 'Czechoslovakia', 'Gilbert Islands (Kiribati)',
                        'Phoenix Islands (Kiribati)', 'Line Islands (Kiribati)']


def add_information_pandas(df, information):
    df = df.copy()
    for key in information:
        df[key] = information[key]
    return df


def preprocess_raw_file_from_MANUAL(config):
    df = config['function']()
    df = add_information_pandas(
        df, {k: v for k, v in config.items() if k != 'function'})

    if 'ISO' not in df.columns:
        df = add_ISO(df)
    if 'Country' in df.columns:
        df = df[~df.Country.isin(exceptions_countries)]
        df = df.drop(columns='Country')
    df['From'] = 'MANUAL'
    return df.dropna(subset=['ISO', 'Value', 'Year'])
