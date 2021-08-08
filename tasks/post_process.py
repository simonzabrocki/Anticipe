import pandas as pd
import numpy as np
import os
import glob
import warnings
warnings.filterwarnings('ignore')

from tasks import compute_index
from index.utils import ISO_to_Everything
from index.GreenGrowthStuff import GreenGrowthStuff

def make_timeseries_excel():
    data = pd.read_csv('data/full_data/result.csv')
    with pd.ExcelWriter('data/results/timeseries.xlsx') as writer:
        for agg in ['Indicator_normed', 'Category', 'Dimension', 'Index']:
            df = data[data.Aggregation == agg]
            variables = df['Variable'].unique()
            for var in variables:
                print(var)
                df_formatted = df[df.Variable == var]
                df_formatted['Year'] = df_formatted['Year'].astype(int)
                df_formatted = df_formatted.pivot(
                    index=['ISO', 'Country', 'Continent', 'UNregion', 'IncomeLevel', 'Region'], columns='Year', values='Value')
                df_formatted = ISO_to_Everything(df_formatted)
                df_formatted = df_formatted[['Country', 'Continent',
                                             'UNregion', 'IncomeLevel',
                                             'Region'] + list(range(2005, 2021))]
                df_formatted.to_excel(writer, sheet_name=var)


def make_imputation_report():
    data = pd.read_csv('data/full_data/data.csv').set_index('ISO')
    data = data[(data.Year >= 2005) & (data.Year <= 2020)]
    data = ISO_to_Everything(data).reset_index()
    ind_cat_dim = GreenGrowthStuff().IND_CAT_DIM
    data = pd.merge(data, ind_cat_dim, on='Indicator')
    data['Year'] = data['Year'].astype(int)
    with pd.ExcelWriter('data/results/imputation_report.xlsx') as writer:
        for agg in [['Continent', 'Dimension'],
                    ['ISO', 'Country', 'Dimension'],
                    ['ISO', 'Country'],
                    ['Continent'],
                    ]:

            df = data.groupby(agg).apply(lambda x: x['Imputed'].sum() / x.shape[0] * 100)
            df = pd.DataFrame(df, columns=['% of imputed data'])
            df['Number of imputed data points'] = data.groupby(
                agg).apply(lambda x: x['Imputed'].sum())

            df['Number of corrected data points'] = data.groupby(
                agg).apply(lambda x: x['Corrected'].sum())

            df['% of corrected data points'] = data.groupby(agg).apply(
                lambda x: x['Corrected'].sum() / x.shape[0] * 100)

            df['Total data points'] = data.groupby(agg).apply(lambda x: x.shape[0])

            df.to_excel(writer, sheet_name='_'.join(agg))


def get_info_from_indictor_df(df):
    
    n_points = df.shape[0]
    n_imputed = df[df.Imputed].shape[0]
    n_corrected = df[df.Corrected].shape[0]
    
    
    earliest_year = df.Year.min()
    latest_year_without_imputation = df[~df.Imputed].Year.max()
    latest_year_with_imputation = df.Year.max()
    
    info = {
            'n_points': n_points,
            '%_imputed': round(n_imputed / n_points * 100, 2),
            '%_outliers': round(n_corrected / n_points * 100, 2),
            'earliest_year': earliest_year,
            'latest_year_without_imputation': latest_year_without_imputation,
            'latest_year_with_imputation': latest_year_with_imputation
           }
    
    return pd.DataFrame([info])


def get_info_from_df(df):
    info_df = df.groupby(['Indicator', 'From']).apply(lambda x: get_info_from_indictor_df(x)).droplevel(2).reset_index()
    return info_df


# def get_info_dataframe():
#     """
#     This function searches for all the files in data/../processed,
#     and returns an excel file with fields of min year, max year, and
#     the number of points for every indicator.
#     """

#     indicators = [file for file in os.listdir('data/indicator') if os.path.isdir(os.path.join('data/indicator', file))]
#     info_df = []

#     for indicator in indicators:

#         raw_path = f'data/indicator/{indicator}/processed/'
#         files = glob.glob(raw_path + "/*.csv")

#         #files = [file for file in files if '.' not in file.split('_')[0]] # remove subindicators

#         for filename in files:

#             df = pd.read_csv(filename, index_col=None)

#             info = get_info_from_dataframe(df)
#             info.update({'file': filename.split('/')[-1], 'indicator': indicator})

#             info_df.append(info)

#     info_df = pd.DataFrame(info_df)

#     info_df = info_df[info_df.file.isin(compute_index.files.values())] # filter only the one used for computation
#     return info_df.reset_index(drop=True)

def get_info_dataframe():
    """
    This function searches for all the files in data/../processed,
    and returns an excel file with fields of min year, max year, and
    the number of points for every indicator.
    """
    data = pd.read_csv('data/full_data/data.csv')
    info_df = get_info_from_df(data)
    return info_df


def reorder_columns(df):
    return df.reindex(sorted(df.columns), axis=1)


def compare_2020_2019_data_report():
    df_2020 = pd.read_csv('data/full_data/data.csv')
    df_2019 = pd.read_csv('data/2019_archive/data.csv')
    
    info_2020 = get_info_from_df(df_2020)
    info_2019 = get_info_from_df(df_2019)
    
    info_df = pd.merge(info_2020, info_2019, on='Indicator', suffixes=('_20', '_19')).set_index('Indicator')

    info_df = reorder_columns(info_df)
    
    return info_df


def correlation_2019_2020_result_report():
    
    data_2019 = pd.read_csv('data/2019_archive/result.csv').assign(version='2019')
    data_2020 = pd.read_csv('data/full_data/result.csv').assign(version='2020')
    data = pd.concat([data_2019, data_2020], axis=0).dropna(subset=['Value'])
    
    pivoted_data = data.pivot(index=['Variable', 'Aggregation', 'Country', 'ISO', 'Year',], columns=['version'], values='Value')
    
    
    by_Variable = pivoted_data.groupby('Variable').apply(lambda x: np.corrcoef(x['2019'].fillna(0), x['2020'].fillna(0))[0, 1])
    corr_by_Variable = pd.DataFrame(by_Variable , columns = {'corr_by_Variable'}).reset_index()
    corr_by_Variable.to_csv('data/results/Correlation_by_variable.csv')
    
    by_Variable_and_Year = pivoted_data.groupby(['Variable', 'Year']).apply(lambda x: np.corrcoef(x['2019'].fillna(0), x['2020'].fillna(0))[0, 1])
    corr_by_Variable_and_Year = pd.DataFrame(by_Variable_and_Year , columns = {'corr_by_Variable_and_Year'} ).reset_index()
    corr_by_Variable_and_Year.to_csv('data/results/Correlation_by_variable_&_Year.csv')
    
    by_Variable_and_country = pivoted_data.groupby(['Variable', 'Country']).apply(lambda x: np.corrcoef(x['2019'].fillna(0), x['2020'].fillna(0))[0, 1])
    corr_by_Variable_and_country = pd.DataFrame(by_Variable_and_country , columns = {'corr_by_Variable_and_country'} ).reset_index()
    corr_by_Variable_and_country.to_csv('data/results/Correlation_by_variable_&_Country.csv')
    
    return corr_by_Variable , corr_by_Variable_and_Year, corr_by_Variable_and_country
 

def make_data_report():
    info_df = get_info_dataframe()
    info_df.to_csv('data/results/data_report.csv', index=False)
