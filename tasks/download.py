import download.downloaders as dd
import os
import json

def download_data_from_config(API_name, config, path, fresh_start):
    existing_files = os.listdir(path)
    file_name = config['GGI_code'] + "_" + API_name + '.json'
    if not fresh_start:
        if file_name not in existing_files:
            dd.download(API_name, config, path=path)
        else:
            print(f'{file_name} already there')
    if fresh_start:
        dd.download(API_name, config, path=path)


def download_data_from_config_dict(download_config, path, fresh_start):
    for API_name, configs in download_config.items():
        for config in configs:
            download_data_from_config(API_name, config, path, fresh_start)


def download_data(fresh_start=False):
    indicators = [file for file in os.listdir('data/indicator') if file != '__init__.py']
    for indicator in indicators:
        config_path = f'data/indicator/{indicator}/download_config.json'
        raw_path = f'data/indicator/{indicator}/raw/'

        print(f"Downloading {indicator}'s data: ")
        try:
            with open(config_path, 'r') as f:
                download_config = json.load(f)
            download_data_from_config_dict(download_config, raw_path, fresh_start)
            print('DONE')
        except Exception as e:
            print(e)
