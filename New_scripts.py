import os
def initialize_indicator(indicator_name):
    
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
initialize_indicator("test_indicator")