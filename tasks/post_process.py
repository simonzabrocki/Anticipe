import pandas as pd
import os
import glob

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
            
            
def get_info_from_dataframe(df):
    
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
    
    return info


def get_info_dataframe():
    """
    This function searches for all the files in data/../processed,
    and returns an excel file with fields of min year, max year, and
    the number of points for every indicator.
    """
    
    indicators = [file for file in os.listdir('data/indicator') if os.path.isdir(os.path.join('data/indicator', file))]
    info_df = []
    
    for indicator in indicators:
        
        raw_path = f'data/indicator/{indicator}/processed/'
        files = glob.glob(raw_path + "/*.csv")
        
        #files = [file for file in files if '.' not in file.split('_')[0]] # remove subindicators
        
        for filename in files:
            
            df = pd.read_csv(filename, index_col=None)
            
            info = get_info_from_dataframe(df)
            info.update({'file': filename.split('/')[-1], 'indicator': indicator})

            info_df.append(info)
            
    info_df = pd.DataFrame(info_df)
            
    info_df = info_df[info_df.file.isin(compute_index.files.values())] # filter only the one used for computation
    return info_df.reset_index(drop=True)


def make_data_report():
    info_df = get_info_dataframe()
    info_df.to_csv('data/results/data_report.csv', index=False)


#  Data report 2019

# Read data
def read_data(file_path):
    data_csv = pd.read_csv(file_path).set_index('ISO')
    return data_csv

def group_data(df):
    info_df = []
    indicato = df.groupby('Indicator')
    indicators = df['Indicator'].unique()
        
    for indicator in indicators:
        each_indicator = indicato.get_group(indicator) 
        earliest_year  = each_indicator.Year.min()
        latest_year  = each_indicator.Year.max()
        data_src = each_indicator.From[0]
        n_points = each_indicator['Indicator'].count()
        try: 
            imputed = round ((( (each_indicator.Imputed.value_counts()[1]) / n_points) * 100), 2)
        except:
            imputed = 0
        try:
            outliers = round((( (each_indicator.Corrected.value_counts()[1]) / n_points) * 100), 2)
        except:
            outliers = 0
        Dict = {"Indicator": indicator , "n_points": n_points, "earliest_year": earliest_year , "latest_year": latest_year , "%_imputed" : imputed , "%_outliers": outliers , "Source":data_src}
        info_df.append(Dict)
    all_data = pd.DataFrame(info_df)
    return all_data
    
def make_data_report_2019():
    info_df = read_data(file_path = 'data/2019_archive/data.csv')
    data_report_2019 = group_data(info_df)
    data_report_2019.to_csv('data/results/data_report_2019.csv', index=False)
