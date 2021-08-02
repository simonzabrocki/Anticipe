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



def get_info_dataframe_2019():
    data = pd.read_csv('data/2019_archive/data.csv').set_index('ISO')

    # indicators
    indicators = data['Indicator']
    corrected = data['Corrected']
    indicators_all = data['Indicator'].unique()    
    min_years = {}
    max_years = {}
    freq = {}
    outl = {}
    imput = {}
    source = {}

    # n_points
    for indicator in indicators:        
        freq[indicator] = freq.get(indicator, 0) + 1 
    
    # min , max years
    for indicator in indicators_all:
        min_years[indicator] = data[data.Indicator.isin([indicator])].Year.min()
        max_years[indicator] = data[data.Indicator.isin([indicator])].Year.max()

    # outliers    
    for indicator in indicators_all:
        try:
            outlier_Per = data[data.Indicator.isin([indicator])].Corrected
            outlier_Perc = round((1 - (outlier_Per.value_counts()[0] / (outlier_Per.value_counts()[0] + outlier_Per.value_counts()[1])))* 100 , 2)
            # outlier_Perc = round((outlier_Per.value_counts()[1] / outlier_Per.value_counts()[0]) * 100, 2) 
            outl[indicator] = outlier_Perc
        except:
            outlier_Perc = 0
            outl[indicator] = outlier_Perc

    # imputation 

    for indicator in indicators_all:
        try:
            imputat_Per = data[data.Indicator.isin([indicator])].Imputed 
            imputat_Perc = round((1 - (imputat_Per.value_counts()[0] / (imputat_Per.value_counts()[0] + imputat_Per.value_counts()[1])))* 100 , 2)
            imput[indicator] = imputat_Perc
        except:
            imputat_Perc = 0
            imput[indicator] = imputat_Perc  

    # source            
    for indicator in indicators_all:
        source[indicator] = data[data.Indicator.isin([indicator])].From.unique()

    # indicator , n_points
    data_INDIC_NPOINTS = pd.DataFrame(list(freq.items()) ,  columns = ['Indicator', 'n_points'])
    data_INDIC_NPOINTS.reset_index(drop = True, inplace=True)

    # latest year , earliest year
    data_YEARS = pd.DataFrame(list(min_years.values()) , list(max_years.values()))
    data_YEARS.reset_index(drop = False, inplace=True)
    data_YEARS.columns = ['latest_year' , 'earliest_year']

    # outliers
    data_OUTLIERS = pd.DataFrame(list(outl.items()) ,  columns = ['Indicator', '%_outliers'])
    data_OUTLIERS.reset_index(drop = True, inplace=True)
    
    # Imputation
    data_Imputation = pd.DataFrame(list(imput.items()) ,  columns = ['Indicator', '%_imputed'])
    data_Imputation.reset_index(drop = True, inplace=True)

    # source
    # Imputation
    data_Source  = pd.DataFrame(list(source.items()) ,  columns = ['Indicator', 'Source'])
    data_Source.reset_index(drop = True, inplace=True)

    # Final
    df = pd.DataFrame()
    df['n_points'] = data_INDIC_NPOINTS['n_points']
    df['%_imputed'] = data_Imputation['%_imputed']
    df['%_outliers'] = data_OUTLIERS['%_outliers']
    df['earliest_year'] = data_YEARS['earliest_year']
    df['latest_year_with_imputation_2020'] = data_YEARS['latest_year']
    df['Source'] = data_Source['Source']
    df['Indicator'] = data_INDIC_NPOINTS['Indicator']
    
    return df


def make_data_report_2019():
    info_df = get_info_dataframe_2019()
    info_df.to_csv('data/2019_archive/data_report.csv', index=False)
