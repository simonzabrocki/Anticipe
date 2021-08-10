from processing.indicator_computation import indicators_computations, compute_from_df
from processing.imputation import impute_data_using_rule, interpolate_linear
from processing.utils import add_Country_from_ISO
from processing.outliers_filtering import filter_outliers
import os
import pandas as pd

indicators = os.listdir('data/indicator')
indicators = [file for file in indicators if len(file) <= 3]


def get_preprocessed_files_from_indicator(indicator):
    path = f'data/indicator/{indicator}'
    files = os.listdir(f'{path}/preprocessed')
    return files


def formatting_step(df):
    df = df.copy()
    df = df.drop(columns='Country', errors='ignore')
    df = add_Country_from_ISO(df)
    df = df.rename(columns={'Variable': 'Indicator'})
    return df  


def process_dataframe(df, indicator):

    print('\t Imputation:', end='')
    try:
        # if indicator == 'SL1':
        #     #df = impute_data_using_rule(df, interpolation_rule_SL1)
        #     df = impute_data_using_rule(df, interpolate_linear)
        # else:
        df = impute_data_using_rule(df, interpolate_linear)
        print('DONE')
    except Exception as e:
        print(e)

    print('\t Outlier removal:', end='')
    try:
        df = filter_outliers(df)
        print('DONE')
    except Exception as e:
        print(e)

    print('\t Formatting:', end='')
    try:
        df = formatting_step(df)
        print('DONE')
    except Exception as e:
        print(e)

    return df


def process_non_computation_file(indicator, file, path, save_path):
    print(f'\t Processing {file}')

    df = pd.read_csv(f'{path}/{file}')
    df = process_dataframe(df, indicator)

    print(f'\t saving at {save_path}/{file}')

    df.to_csv(f'{save_path}/{file}', index=False)


def process_computation_files(indicator, path, save_path):
    '''Immondice à nettoyer'''
    for file, config in indicators_computations[indicator]:
        sub_indicator_files = config['files']
        sub_indicator_dfs = [pd.read_csv(
            f'{path}/{file}') for file in sub_indicator_files]
        print(
            f"\t Processing sub indicators from {', '.join(sub_indicator_files)}")
        sub_indicator_dfs = [process_dataframe(
            df, indicator) for df in sub_indicator_dfs]

        for i, df in enumerate(sub_indicator_dfs):
            formatting_step(df).to_csv(
                f'{save_path}/{sub_indicator_files[i]}', index=False)

        print(f'\t Computing {indicator} for {file}', end=': ')
        try:
            df = compute_from_df(pd.concat(sub_indicator_dfs), config)
            print('DONE')
        except Exception as e:
            print(e)

        df = process_dataframe(df, indicator)
        
        print(f'saving at {save_path}/{file}')
        df.to_csv(f'{save_path}/{file}', index=False)


def get_from_to_path(indicator):
    return f'data/indicator/{indicator}/preprocessed', f'data/indicator/{indicator}/processed'


def process_indicator(indicator):
    print(f'Processing {indicator}: ')

    preprocessed_files = get_preprocessed_files_from_indicator(indicator)
    path, save_path = get_from_to_path(indicator)

    if indicator in indicators_computations:
        process_computation_files(indicator, path, save_path)

    else:
        for file in preprocessed_files:
            process_non_computation_file(indicator, file, path, save_path)


def process_indicators():
    for indicator in indicators:
        process_indicator(indicator)
