from processing.api_preprocessors import preprocess_file_from_api
from processing.manual_preprocessors import preprocess_raw_file_from_MANUAL, MANUAL_CONFIGS
import os


# APIs
def preprocess_APIs_data_in_indicator(indicator):
    path = f'data/indicator/{indicator}'
    API_files = [file for file in os.listdir(f'{path}/raw') if '.M.' not in file]
    for file in API_files:
        raw_path = f'{path}/raw/{file}'
        file = '.'.join(file.split('.')[:-1]) + '.csv'
        preprocess_path = f'{path}/preprocessed/{file}'

        print(f'PreProcessing {raw_path}', end=': ')
        try:
            df = preprocess_file_from_api(raw_path)
            print(f'Saving at {preprocess_path}')
            df.to_csv(preprocess_path, index=False)
            print('Done')
        except Exception as e:
            print('Error: ', e)


def preprocess_API_files():
    excluded = ["__pycache__", '__init__.py']
    indicators = [file for file in os.listdir('data/indicator') if file not in excluded]
    for indicator in indicators:
        preprocess_APIs_data_in_indicator(indicator)


# MANUALs        
def preprocess_MANUAL_data_in_indicator(indicator):
    config = MANUAL_CONFIGS.get(indicator, None)
    print(f"PreProcessing {indicator} Manual files", end=': ')
    try:
        df = preprocess_raw_file_from_MANUAL(config)
        preprocess_path = f'data/indicator/{indicator}/preprocessed/{indicator}_origin.M.csv'
        print(f'Saving at {preprocess_path}')
        df.to_csv(preprocess_path, index=False)
        print('Done')
    except Exception as e:
        print('Error: ', e)
    

def preprocess_MANUAL_files():
    for indicator in MANUAL_CONFIGS.keys():
        preprocess_MANUAL_data_in_indicator(indicator)

