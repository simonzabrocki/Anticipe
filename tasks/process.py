import os
import pandas as pd
from processing.imputation import impute_data_using_rule, interpolation_rule_SL1, interpolate_linear
from processing.utils import add_Country_from_ISO
from processing.outliers_filtering import filter_outliers

indicators = os.listdir('data/indicator')
indicators = [file for file in indicators if len(file) <= 3]


def get_preprocessed_files_from_indicator(indicator):
    path = f'data/indicator/{indicator}'
    folder = os.listdir(path)
    if 'computed' in folder:
        files = os.listdir(f'{path}/computed')
        return [(file, indicator, 'computed') for file in files]
    else:
        files = os.listdir(f'{path}/preprocessed')
        return [(file, indicator, 'preprocessed') for file in files]


def get_preprocessed_files(indicators):
    files = [get_preprocessed_files_from_indicator(indicator) for indicator in indicators]
    files = [item for sublist in files for item in sublist]
    return files


def formatting_step(df):
    df = df.copy()
    df = df.drop(columns='Country', errors='ignore')
    df = add_Country_from_ISO(df)
    df = df.rename(columns={'Variable': 'Indicator'})
    return df


def process_files():
    '''Processing Script'''
    preprocessed_files = get_preprocessed_files(indicators)

    for file, indicator, folder in preprocessed_files:

        print(f'Processing {file}: ')

        df = pd.read_csv(f'data/indicator/{indicator}/{folder}/{file}')
        save_path = f'data/indicator/{indicator}/processed/{file}'

        # Imputation
        print('Imputation:', end='')
        try:
            if indicator == 'SL1':
                df = impute_data_using_rule(df, interpolation_rule_SL1)
            else:
                df = impute_data_using_rule(df, interpolate_linear)
            print('DONE')
        except Exception as e:
            print(e)

        # Outlier Removal
        print('Outlier removal:', end='')
        try:
            df = filter_outliers(df)
            print('DONE')
        except Exception as e:
            print(e)

        # Formatting
        print('Formatting:', end='')
        try:
            df = formatting_step(df)
            print('Done')
        except Exception as e:
            print(e)

        # Saving
        print(f'saving at {save_path}: ', end='')
        try:
            df = df.to_csv(save_path, index=False)
            print('Done')
        except Exception as e:
            print(e)

    return None


if __name__ == '__main__':
    process_files()
