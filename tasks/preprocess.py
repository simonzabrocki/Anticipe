from data.indicator.GN1.preprocess import process_GN1
from data.indicator.CV2.preprocess import process_CV2
from data.indicator.EQ2.preprocess import process_EQ2
from data.indicator.EQ3.preprocess import process_EQ3
from data.indicator.GB3.preprocess import process_GB3
from data.indicator.GJ1.preprocess import process_GJ1
from data.indicator.GT1.preprocess import process_GT1
from data.indicator.ME1.preprocess import process_ME1
from data.indicator.ME2.preprocess import process_ME2
from data.indicator.SL1.preprocess import process_SL1
from data.indicator.SL2.preprocess import process_SL2
from data.indicator.SP2.preprocess import process_SP2

from processing.utils import add_ISO
from processing.api_preprocessors import preprocess_file_from_api
import os


# APIs
def process_APIs_data_in_indicator(indicator):
    path = f'data/indicator/{indicator}'
    API_files = [file for file in os.listdir(f'{path}/raw') if '.M.' not in file]
    for file in API_files:
        raw_path = f'{path}/raw/{file}'
        preprocess_path = f'{path}/preprocessed/'
        preprocess_file_from_api(raw_path, preprocess_path)


def process_APIs_raw_data():
    indicators = [file for file in os.listdir('data/indicator') if file != '__init__.py']

    for indicator in indicators:
        try:
            process_APIs_data_in_indicator(indicator)
        except Exception as e:
            print(e)


# MANUAL
manual_configs = [
    {
        'Variable': 'ME2',
        'function': process_ME2,
        'Description': 'Total material footprint (MF) per capita',
        'Source': 'U.N. Environment: Secretariat of the International Resource Panel',
        'URL': 'https://www.resourcepanel.org/global-material-flows-database'
    },
    {
        'Variable': 'SL1',
        'function': process_SL1,
        'Description': 'Average soil organic carbon content',
        'Source': 'FAO',
        'URL': 'http://54.229.242.119/GSOCmap/'
    },
    {
        'Variable': 'SL2',
        'function': process_SL2,
        'Description': 'Share agriculture organic to total agriculture land area (Percent)',
        'Source': 'FAOSTAT',
        'URL': 'http://www.fao.org/faostat/en/#data/EL'
    },
    {
        'Variable': 'GJ1',
        'function': process_GJ1,
        'Description': 'Share of green manufacturing employment in total manufacturing employment',
        'Source': 'Valentin Todorov',
        'URL': ''
    },
    {
        'Variable': 'EQ2',
        'function': process_EQ2,
        'Description': 'DALYs (Disability-Adjusted Life Years), Rate, Age-standardized, Unsafe water source',
        'Source': 'GHD',
        'URL': 'http://ghdx.healthdata.org/gbd-results-tool?params=gbd-api-2017-permalink/b6989accc192c6a5f121a8204b88f819'
    },
    {
        'Variable': 'GN1',
        'function': process_GN1,
        'Description': 'Cumulative Share of patent publications in environmental technology to total patents',
        'Source': 'World Intellectual Property Organization (WIPO) statistics database',
        'URL': 'https://www3.wipo.int/ipstats/index.htm?tab=patent'
    },
    {
        'Variable': 'SP2',
        'function': process_SP2,
        'Description': 'Health care Access and Quality Index',
        'Source': 'Institute for Health Metrics and Evaluation, based on Global Burden of Disease Study 2015 (GBD 2015).',
        'URL': 'http://ghdx.healthdata.org/record/global-burden-disease-study-2015-gbd-2015-healthcare-access-and-quality-index-based-amenable'
    },
    {
        'Variable': 'GT1',
        'function': process_GT1,
        'Description': 'Share of export of environmental goods (OECD and APEC classifications) to total export (%)',
        'Source': 'UNCOMTRADE data and OECD and APEC classifications of environmental goods',
        'URL': 'https://comtrade.un.org/data/'
    },
    {
        'Variable': 'EQ3',
        'function': process_EQ3,
        'Description': 'Municipal solid waste (MSW) generation per capita tons per capita',
        'Source': 'World Bank What a Waste database',
        'URL': 'https://datacatalog.worldbank.org/dataset/what-waste-global-database'
    },
    {
        'Variable': 'CV2',
        'function': process_CV2,
        'Description': 'Tourism and recreation in coastal and marine areas score',
        'Source': 'Ocean Health Index',
        'URL': 'http://ohi-science.org/ohi-global/download'
    },
    {
        'Variable': 'GB3',
        'function': process_GB3,
        'Description': 'Getting paid, laws and regulations for equal gender pay score',
        'Source': 'World Bank Women, Business and the Law',
        'URL': 'http://wbl.worldbank.org/en/reports'
    },
    {
        'Variable': 'ME1',
        'function': process_ME1,
        'Description': 'Total domestic material consumption (DMC) per unit of GDP',
        'Source': 'Environment Live / Global Material Flows Database',
        'URL': 'https://unstats.un.org/sdgs/indicators/database/'
    }
]


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
    df = add_information_pandas(df, {k: v for k, v in config.items() if k != 'function'})

    if 'ISO' not in df.columns:
        df = add_ISO(df)
    if 'Country' in df.columns:
        df = df[~df.Country.isin(exceptions_countries)]
        df = df.drop(columns='Country')
    df['From'] = 'MANUAL'
    return df.dropna(subset=['ISO', 'Value', 'Year'])


def preprocess_MANUAL_files():
    for config in manual_configs:
        indicator = config['Variable']
        print(f"PreProcessing {indicator} Manual files", end=': ')
        try:
            df = preprocess_raw_file_from_MANUAL(config)
            df.to_csv(f'data/indicator/{indicator}/preprocessed/{indicator}_origin.M.csv', index=False)
            print('DONE')
        except Exception as e:
            print(e)
