from tasks.pipeline import indicator_pipeline
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a new indicator.')
    parser.add_argument('--name', type=str, help='The indicator name')
    name = parser.parse_args().name
    indicator_pipeline(name)
