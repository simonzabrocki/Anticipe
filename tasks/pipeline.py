from tasks.download import download_indicator
from tasks.preprocess import preprocess_APIs_data_in_indicator, preprocess_MANUAL_data_in_indicator
from tasks.process import process_indicator


def indicator_pipeline(indicator, fresh_start=True):
    
    print(f'Downloading..')
    download_indicator(indicator, fresh_start)
    
    print('Preprocessing...')
    preprocess_MANUAL_data_in_indicator(indicator)
    preprocess_APIs_data_in_indicator(indicator)
    
    print('Processing...')
    process_indicator(indicator)
    
