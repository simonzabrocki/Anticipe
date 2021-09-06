import pandas as pd
import os
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


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
                min_year = int(df.Year.min())
                df_formatted['Year'] = df_formatted['Year'].astype(int)
                df_formatted = df_formatted.pivot(
                    index=['ISO', 'Country', 'Continent', 'UNregion', 'IncomeLevel', 'Region'], columns='Year', values='Value')
                df_formatted = ISO_to_Everything(df_formatted)
                df_formatted = df_formatted[['Country', 'Continent',
                                             'UNregion', 'IncomeLevel',
                                             'Region'] + list(range(min_year, 2021))]
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
    #description = df.Description.unique()[0]
    
    n_ISO = df.ISO.unique().shape[0]
    
    earliest_year = df.Year.min()
    latest_year_without_imputation = df[~df.Imputed].Year.max()
    latest_year_with_imputation = df.Year.max()
    
    info = {
            #'Description': description,
            'n_points': n_points,
            'n_ISO': n_ISO,
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


def make_2019_2020_correlation_report():
    
    data_2019 = pd.read_csv('data/2019_archive/result.csv').assign(version='v_2019')
    data_2020 = pd.read_csv('data/full_data/result.csv').assign(version='v_2020')
    data = pd.concat([data_2019, data_2020], axis=0).dropna(subset=['Value'])
    ISO_with_index = data.query("Aggregation == 'Index'").dropna().ISO.unique() # Select only ISOs where the full index is computed to remove some noise
    data = data[data.ISO.isin(ISO_with_index)]
    
    pivoted_data = data.pivot(index=['Variable', 'Aggregation', 'ISO', 'Year'], columns=['version'], values='Value')
    
    corr_by_var = pivoted_data.groupby(['Variable', 'Aggregation']).apply(lambda x: x[['v_2019', 'v_2020']].dropna().corr().values[0, 1]).to_frame(name='corr')
    corr_by_var_ISO = pivoted_data.groupby(['Variable', 'Aggregation', 'ISO']).apply(lambda x: x[['v_2019', 'v_2020']].dropna().corr().values[0, 1]).to_frame(name='corr')

    return pivoted_data, corr_by_var.reset_index(), corr_by_var_ISO.reset_index()


def make_data_report():
    info_df = get_info_dataframe()
    info_df.to_csv('data/results/data_report.csv', index=False)



def make_indicator_box_plots():
    data = pd.read_csv('data/full_data/result.csv')
    IND_CAT_DIM = GreenGrowthStuff().IND_CAT_DIM
    plot_df = (
        data.query("Aggregation == 'Indicator' and Year == 2020 ")
             .merge(IND_CAT_DIM, left_on='Variable', right_on='Indicator')
    )

    for category in plot_df.Category.unique():
        fig = px.box(plot_df.query(f'Category == "{category}"'), y='Value', points="all" ,hover_data=['ISO', 'Country'], facet_col='Variable', facet_col_wrap=3).update_yaxes(matches=None, showticklabels=True)
        fig.write_html(f"plots/{category}_boxplot.html")

    return None


def make_indicator_correlation_matrix():
    data = pd.read_csv('data/full_data/result.csv')
    IND_CAT_DIM = GreenGrowthStuff().IND_CAT_DIM
    plot_df = (
        data.query("Aggregation == 'Indicator' and Year == 2020 ")
             .merge(IND_CAT_DIM, left_on='Variable', right_on='Indicator')
    )
    
    corr = plot_df.pivot(index=['ISO', 'Year'], columns=['Variable'], values='Value').corr()
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(corr, annot=False, center=0, linewidths=.01, ax=ax, cmap='coolwarm')
    plt.savefig('plots/indicator_corrmatrix.png')
    return None


def make_indicator_correlation_matrix():
    data = pd.read_csv('data/full_data/result.csv')
    IND_CAT_DIM = GreenGrowthStuff().IND_CAT_DIM
    plot_df = (
        data.query("Aggregation == 'Indicator' and Year == 2020 ")
             .merge(IND_CAT_DIM, left_on='Variable', right_on='Indicator')
    )
    
    
    for dim in ['ESRU', 'NCP', 'GEO', 'SI']:
        
        corr = plot_df.query('Dimension == @dim').pivot(index=['ISO', 'Year'], columns=['Variable'], values='Value').corr()
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(corr, annot=False, center=0, linewidths=.01, ax=ax, cmap='coolwarm')
        plt.savefig(f'plots/{dim}_indicator_corrmatrix.png')
    return None

