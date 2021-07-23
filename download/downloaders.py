import abc
import requests
import json
from datetime import date
import wbdata
from colorama import Fore, init


class Downloader(metaclass=abc.ABCMeta):
    '''
    Abstract class used to download data coming from an API
    '''
    def __init__(self, API_URL):
        self.API_URL = API_URL
        return None

    @abc.abstractmethod
    def get_raw_data(self, params):
        '''
        Download the raw data

        Parameters
        ---------
        params: dictionnary
            dictionnary with the API parameters
        '''
        pass

    def get_data(self, params):
        '''
        Fetch the raw data and add timestamp and origin

        Parameters
        ---------
        params: dictionnary
            dictionnary with the API parameters
        '''
        data = self.get_raw_data(params)

        p = requests.Request('GET', self.API_URL, params=params).prepare().url
        metadata = {'URL': p, 'DownloadDate': str(date.today())}
        result = {}
        result['data'] = data
        result['metadata'] = metadata

        return result

    def download_data(self, path, params):
        '''
        Fetch the data and save it at path

        Parameters
        ---------
        path: str
            Path to save file
        params: dictionnary
            dictionnary with the API parameters
        '''

        data = self.get_data(params)

        with open(path, 'w') as file:
            json.dump(data, file)

        return data


class CW_Downloader(Downloader):
    '''
    Class to download data coming from CW API
    '''
    def get_raw_data(self, params):
        first_request = requests.get(self.API_URL, params=params)
        data = first_request.json()['data']

        if 'next' in first_request.links.keys():
            has_next = True
            next_url = first_request.links['next']['url']
        else:
            has_next = False

        while has_next:
            next_request = requests.get(next_url)
            data += (next_request.json()['data'])

            if 'next' in next_request.links.keys():
                next_url = next_request.links['next']['url']
            else:
                has_next = False

        return data
    
    

    def get_CW_API_ids(self, query_param, API_URL='https://www.climatewatchdata.org/'):
        """

        """            
        url     = f'{API_URL}/api/v1/data/historical_emissions/{query_param}'

        response = requests.get(url, params=query_param, headers={"Accept": "application/json"})


        data_json = response.json()
        df = pd.json_normalize(data_json['data']) 

        return df


class SDG_Downloader(Downloader):
    '''
    Class to download data coming from SDG API
    '''
    def get_raw_data(self, params):

        params['pageSize'] = int(1e9)  # Set large number to get all the data, avoid 2 calls
        request = requests.get(self.API_URL, params=params)
        data = request.json()['data']
        return data


class WB_Downloader(Downloader):
    '''
    Class to download data coming from WB API
    '''
    def get_raw_data(self, params):
        indicator = params['indicator']
        url = f'{self.API_URL}/{indicator}'
        params = {'format': 'json', 'per_page': 1}

        # request to get the number of element and make a full request
        pre_request = requests.get(url, params=params)
        total = pre_request.json()[0]['total']
        params['per_page'] = total

        # actual request
        request = requests.get(url, params=params)

        data = request.json()

        # add source
        data[0]['Source'] = wbdata.get_indicator(indicator)[0]['sourceOrganization']  # Well maybe we could just use wbdata alltogether :/

        return data


#############


API_CONFIGS = {
    'WB': {
        'API': 'WB API',
        'downloader': WB_Downloader('https://api.worldbank.org/v2/country/all/indicator/'),
    },
    'SDG': {
        'API': 'SDG API',
        'downloader': SDG_Downloader('https://unstats.un.org/SDGAPI/v1/sdg/Series/Data'),
    },
    'CW': {
        'API': 'CW API',
        'downloader': CW_Downloader('https://www.climatewatchdata.org/api/v1/data/historical_emissions'),
    }
}

init(autoreset=True)


def download(API_name, config, path=None, restart=False, API_CONFIGS=API_CONFIGS):
    '''
    Wrapper function for downloading and preprocessing data from API.
    This is used in the command line tool. For specific uses, use the individual downloaders and preprocessors.

    Parameters
    ----------
    API_name: str
        The name of the API
    config: dict
        A dictionnary with keys 'GGI_code' and 'params'.
    path: str
        Path for saving
    raw: Bool
        whether to download the raw data or the preprocessed one.
    API_CONFIGS:
        The configs of the APIs
    '''
    assert API_name in ['CW', 'SDG', 'WB'], f"{API_name} is not in {['CW', 'SDG', 'WB']}"

    # SET UP PARAMATERS
    params = config['params']
    GGI_code = config['GGI_code']
    Downloader = API_CONFIGS[API_name]['downloader']
    file_path = f"{path}{GGI_code}_{API_name}.json"

    # DOWNLOADING
    print(f'Downloading {config} from {API_name}', end=': ')
    try:
        data = Downloader.get_data(params)
        data['metadata']['GGI_code'] = GGI_code
        data['metadata']['API_name'] = API_name + ' API'

        print(Fore.GREEN + 'DONE')
    except Exception as e:
        print(Fore.RED + 'Error occured ', e)

    # SAVING

    print(f'Saving at {file_path}', end=': ')
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(Fore.GREEN + 'DONE')
    except Exception as e:
        print(Fore.RED + 'Error occured ', e)

    return data
