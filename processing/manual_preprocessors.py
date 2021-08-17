from processing.utils import add_ISO


#from data.indicator.CV2.preprocess import config_CV2
#from data.indicator.EQ2.preprocess import config_EQ2
#from data.indicator.EQ3.preprocess import config_EQ3
#from data.indicator.GB3.preprocess import config_GB3
#from data.indicator.GJ1.preprocess import config_GJ1
#from data.indicator.GN1.preprocess import config_GN1
#from data.indicator.GT1.preprocess import config_GT1
#from data.indicator.ME1.preprocess import config_ME1
#from data.indicator.ME2.preprocess import config_ME2
#from data.indicator.SL1.preprocess import config_SL1
#from data.indicator.SL2.preprocess import config_SL2
#from data.indicator.SP2.preprocess import config_SP2
#from data.indicator.GS2.preprocess import config_GS2


from data.indicator import (CV2, EQ2, EQ3, GB3,
                            GJ1, GN1, GT1, ME1,
                            ME2, SL1, SL2, SP2, GS2)


# MANUAL 

MANUAL_CONFIGS = {
    'CV2': CV2.config,
    'EQ2': EQ2.config,
    'EQ3': EQ3.config,
    'GB3': GB3.config,
    'GJ1': GJ1.config,
    'GN1': GN1.config,
    'GT1': GT1.config,
    'ME1': ME1.config,
    'ME2': ME2.config,
    'SL1': SL1.config,
    'SL2': SL2.config,
    'SP2': SP2.config,
    'GS2': GS2.config,
    
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
