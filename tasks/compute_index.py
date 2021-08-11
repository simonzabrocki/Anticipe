import os
import pandas as pd
from index.IndexComputation.GreenGrowthIndex import GreenGrowthIndex
from index.utils import ISO_to_Everything


indicators = os.listdir('data/indicator')
indicators = [file for file in indicators if len(file) <= 3]
ST = pd.read_csv('data/sustainable_targets/ST_2020.csv', index_col=0)


files = {'AB1': 'AB1_SDG.csv',
         'AB2': 'AB2_SDG.csv',
         'AB3': 'AB3.csv',
         'BE1': 'BE1.csv',
         'BE2': 'BE2_WB.csv',
         'BE3': 'BE3_SDG.csv',
         'CV1': 'CV1_SDG.csv',
         'CV2': 'CV2_origin.M.csv',
         'CV3': 'CV3_WB.csv',
         'EE1': 'EE1_SDG.csv',
         'EE2': 'EE2_SDG.csv',
         'EQ1': "EQ1_WB.csv",
         'EQ2': 'EQ2_origin.M.csv',
         'EQ3': 'EQ3_origin.M.csv',
         'EW1': 'EW1_SDG.csv',
         'EW2': 'EW2_SDG.csv',
         'GB1': 'GB1_SDG.csv',
         'GB2': 'GB2_SDG.csv',
         'GB3': 'GB3_origin.M.csv',
         'GE1': 'GE1.csv',
         'GE2': 'GE2.csv',
         'GE3': 'GE3.csv',
         'GJ1': 'GJ1_origin.M.csv',
         'GN1': 'GN1_origin.M.csv',
         'GT1': 'GT1_origin.M.csv',
         'GV1': 'GV1_WB.csv',
         'ME1': 'ME1_origin.M.csv',
         #'ME1': 'ME1_SDG.csv',
         'ME2': 'ME2_origin.M.csv',
         'SE1': 'SE1.csv',
         'SE2': 'SE2_SDG.csv',
         'SE3': 'SE3_SDG.csv',
         'SL1': 'SL1_origin.M.csv',
         'SL2': 'SL2_origin.M.csv',
         'SP1': 'SP1_SDG.csv',
         #'SP2': 'SP2_origin.M.csv',
         'SP2': 'SP2_SDG.csv',
         'SP3': 'SP3_SDG.csv'
         }


def get_df_from_processed_files(files):
    dfs = []
    for indicator, file in files.items():
        dfs.append(pd.read_csv(f'data/indicator/{indicator}/processed/{file}'))
    df = pd.concat(dfs)
    df = df.dropna(subset=['Year'])
    return df


def format_df_for_computation(df):
    df = df.pivot(index=['ISO', 'Year'], columns='Indicator', values='Value').reset_index()
    df.columns.name = None
    df = df.set_index('Year')
    return df


def compute_index_from_df(df, save):
    GGIs = []
    for year in range(2005, 2021):
        indicators = df.loc[year].reset_index(drop=True).set_index('ISO')
        indicators.columns.name = None
        GGI = GreenGrowthIndex(indicators=indicators, sustainability_targets=ST)
        if save:
            print(f"Saving {year}'s results")
            GGI.to_excel(f'data/results/result_{year}.xlsx')

        GGI = GGI.to_long()
        GGI['Year'] = year
        GGIs.append(GGI)

    GGIs = pd.concat(GGIs, axis=0)

    data = ISO_to_Everything(GGIs).reset_index()

    return data


def compute_index(save=False):
    print('Computing Index:')

    print('Collecting data:', end='')
    try:
        path = 'data/full_data/data.csv'
        df = get_df_from_processed_files(files).drop(columns=['Description', 'URL', 'DownloadDate']) # To cleanup later
        df.to_csv(path, index=False)
        print(f'Saving at {path}')
    except Exception as e:
        print(e)
    print('Computation: ', end='')
    try:
        path = 'data/full_data/result.csv'
        df = format_df_for_computation(df)
        data = compute_index_from_df(df, save)
        data.to_csv(path, index=False)

        print(f'saving at {path}')
    except Exception as e:
        print(e)
