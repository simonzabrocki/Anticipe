import os
import argparse


def initialize_indicator(indicator_name):

    assert indicator_name not in os.listdir('data/indicator/'), f"indicator {indicator_name} already exists"
    assert len(indicator_name) == 3, 'indicator name must have 3 characters'

    directory = indicator_name
    parent_dir = f"data/indicator/"
    path = os.path.join(parent_dir, directory)

    try: 
        os.mkdir(path)
        print("Indicator '% s' created" % directory)
    except OSError as error:
        print(error)  
    # Create sub directories and files
    newp = os.chdir(path)
    try:
        [os.mkdir(dir) for dir in ['preprocessed', 'processed' , 'raw']]
    except OSError as error:
        print(error)     

    files = ['config.json' , 'download_config.json', 'preprocess.py', 'process.py']
    for file in files:
        with open( file,  'w') as fp:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize a new indicator.')
    parser.add_argument('--name', type=str, help='The indicator name')

    name = parser.parse_args().name

    initialize_indicator(name)
