import abc
import pandas as pd
from processing.utils import add_ISO
import json
import numpy as np

from data.indicator.GE1.preprocess import process_GE1_0
from data.indicator.GE2.preprocess import process_GE2_0
from data.indicator.GE3.preprocess import process_GE3_1


class Preprocessor(metaclass=abc.ABCMeta):
    '''
    Abstract processor class used to preprocess data coming from API

    Attributes
    ----------
    variable: str
        Name of the variable to be preprocessed (Used to handle special cases)
    '''

    def __init__(self, variable):
        self.variable = variable
        return None

    def parse_json(self, json):
        '''
        Parse the json file

        Parameters
        ---------
        json: list of dictionnary
            The loaded json file
        '''
        metadata_json = json['metadata']
        data_json = json['data']

        return metadata_json, data_json

    @abc.abstractmethod
    def json_to_pandas(self, data_json):
        '''
        Convert the json to pandas

        Parameters
        ---------
        data_json: list of dictionnary
            The data from the json file
        '''
        pass

    @abc.abstractmethod
    def format_pandas(self, df):
        '''
        Format the raw pandas

        Parameters
        ---------
        df: pd.DataFrame
            Raw DataFrame
        '''
        pass

    @abc.abstractmethod
    def convert_dtypes(self, df):
        pass

    @abc.abstractmethod
    def handle_exceptions(self, df):
        pass

    def add_information_pandas(self, df, metadata_json):
        '''
        Add information to the pandas

        Parameters
        ---------
        df: pd.DataFrame
            Formated DataFrame
        metadata_json: dict
            A dictionnary with the information to add (eg. download data, variable name etc ...)

        Returns
        -------
        df: pd.DataFrame
        '''
        df = df.copy()
        for key in metadata_json:
            df[key] = metadata_json[key]
        return df

    def preprocess(self, data_json):
        '''
        Preprocess a given json file and complete with the relevant information

        Parameters
        ---------
        ddata_json: json
            Raw loaded json file
        information: dict
            A dictionnary with the information to add (eg. download data, variable name etc ...)

        Returns
        -------
        df: pd.DataFrame
        '''
        metadata_json, df = self.parse_json(data_json)
        for step in [self.json_to_pandas, self.handle_exceptions, self.format_pandas, self.convert_dtypes]:
            df = step(df)

        final_df = self.add_information_pandas(df, metadata_json)
        final_df = final_df.rename(columns={'GGI_code': 'Variable', 'API_name': 'From'})
        return final_df.dropna().drop_duplicates()


class SDG_Preprocessor(Preprocessor):
    '''
    Processor class used to preprocess data coming from SDG API
    '''

    def json_to_pandas(self, json):
        df = pd.json_normalize(json)
        columns = df.columns
        dimensions = [dim for dim in columns if 'dimensions' in dim]
        to_select = ['seriesDescription', 'geoAreaName',
                     'source', 'timePeriodStart', 'value'] + dimensions
        df = df[to_select]
        return df

    def format_pandas(self, df):
        df = df.copy()
        df = df.rename(columns={'geoAreaName': 'Country',
                                'timePeriodStart': 'Year',
                                'value': 'Value',
                                'seriesDescription': 'Description',
                                'source': 'Source'
                                }
                       )
        columns = df.columns
        dimensions = [dim for dim in columns if 'dimensions' in dim]

        for dim in dimensions:
            df['Description'] += ' ' + dim.split('.')[1] + ' ' + df[dim]

        df = add_ISO(df)
        return df.drop(columns=dimensions)

    def convert_dtypes(self, df):
        df = df.copy()

        df['Year'] = df['Year'].astype(int)
        df['Value'] = df['Value'].astype(float)

        return df

    def handle_exceptions(self, df):
        excluded = [
            "Northern Africa (exc. Sudan)",
            "Micronesia",
            "Southern Africa",
            "Sudan [former]"
        ]

        df = df[~df.geoAreaName.isin(excluded)]
        if self.variable == 'AB2.1':
            df = df.copy()
            df.loc[df['value'] == '>95', 'value'] = 95
            df.loc[df['value'] == '<5', 'value'] = 5
            return df
        if self.variable == 'EW3':
            df = df.copy()
            df.loc[df['value'] == 'N', 'value'] = np.nan
            return df
        if self.variable == 'ME3.2':
            df = df.copy()
            df['value'] = df['value'].astype(float)
            return df
        else:
            return df


class WB_Preprocessor(Preprocessor):
    '''
    Processor class used to preprocess data coming from WB API
    '''

    def json_to_pandas(self, data_json):
        df = pd.json_normalize(data_json[1])
        df['Source'] = data_json[0]['Source']

        return df

    def format_pandas(self, df):
        df = df.rename(columns={'countryiso3code': 'ISO',
                                'date': 'Year',
                                'value': 'Value',
                                'indicator.value': 'Description',
                                'country.value': 'Country'})

        df = df.drop(columns=['obs_status', 'unit', 'decimal', 'indicator.id', 'country.id'])
        df = df.replace(r'^\s*$', np.nan, regex=True)
        return df

    def convert_dtypes(self, df):
        return df

    def handle_exceptions(self, df):
        df = df.query("countryiso3code != 'AFE'")
        return df


class CW_Preprocessor(Preprocessor):
    '''
    Processor class used to preprocess data coming from CW API
    '''

    def dict_to_df(self, dictionnary):
        '''
        Convert a dict to a dataframe

        Parameters
        ---------
        dictionnary: dictionnary
            dictionnary output by the CW API
        '''
        df = pd.DataFrame(dictionnary['emissions'])

        for key in dictionnary.keys():
            if key != 'emissions':
                df[key] = dictionnary[key]

        return df

    def json_to_pandas(self, data_json):
        return pd.concat([self.dict_to_df(d) for d in data_json], axis=0)

    def handle_exceptions(self, df):
        return df

    def format_pandas(self, df):
        df = df.rename(columns={'year': 'Year', 'value': 'Value',
                                'iso_code3': 'ISO', 'data_source': 'Source', 'country': 'Country'})

        if self.variable == 'GE1.0':
            df = process_GE1_0(df)
        if self.variable == 'GE2.0':
            df = process_GE2_0(df)
        if self.variable == 'GE3.1':
            df = process_GE3_1(df)
        df = df.drop(columns=['id'], errors='ignore')

        return df

    def convert_dtypes(self, df):
        return df


PROCESSING_CONFIGS = {
    'WB API': {
        'preprocessor': WB_Preprocessor,
    },
    'SDG API': {
        'preprocessor': SDG_Preprocessor,
    },
    'CW API': {
        'preprocessor': CW_Preprocessor,
    }
}


def preprocess_raw_dict(dictionnary, preprocessor):
    GGI_code = dictionnary['metadata']['GGI_code']
    preprocessor = preprocessor(GGI_code)
    df = preprocessor.preprocess(dictionnary)
    return df


def preprocess_file_from_api(raw_file_path, PROCESSING_CONFIGS=PROCESSING_CONFIGS):

    with open(f'{raw_file_path}', 'r') as outfile:
        data = json.load(outfile)

    API = data['metadata']['API_name']
    preprocessor = PROCESSING_CONFIGS[API]['preprocessor']
    df = preprocess_raw_dict(data, preprocessor)

    return df

# def preprocess_file_from_api(raw_file_path, preprocess_path, PROCESSING_CONFIGS=PROCESSING_CONFIGS):
#     with open(f'{raw_file_path}', 'r') as outfile:
#         data = json.load(outfile)
#
#     API = data['metadata']['API_name']
#     GGI_code = data['metadata']['GGI_code']
#
#     preprocessor = PROCESSING_CONFIGS[API]['preprocessor']
#     file_path = f"{preprocess_path}{GGI_code}_{API.split(' ')[0]}.csv"
#
#     print(f'PreProcessing {raw_file_path}', end=': ')
#     try:
#         df = preprocess_raw_dict(data, preprocessor)
#         df.dropna(subset=['ISO']).to_csv(file_path, index=False)
#         print('DONE')
#
#     except Exception as e:
#         print('Error occured ', e)
#     return df
