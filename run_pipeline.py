import argparse

from tasks.download import download_data
from tasks.preprocess import preprocess_MANUAL_files, preprocess_API_files
from tasks.compute_indicators import compute_indicators
from tasks.process import process_indicators
from tasks.compute_index import compute_index 



def get_parser():
    parser = argparse.ArgumentParser(description='Run the green growth index pipeline.')
    parser.add_argument('--step', type=str, help='The step to run')


    return parser

if __name__ == "__main__":
    parser = get_parser()

    pipeline_steps = {
        "download": [download_data],
        "preprocess": [preprocess_MANUAL_files, preprocess_API_files],
        "compute_indic": [compute_indicators],
        "process": [process_indicators],
        "compute": [compute_index],
        "all": [download_data, preprocess_MANUAL_files, preprocess_API_files, process_indicators, compute_index]
    }

    step = parser.parse_args().step

    steps_to_run = pipeline_steps[step]

    for func in steps_to_run:
        func()

