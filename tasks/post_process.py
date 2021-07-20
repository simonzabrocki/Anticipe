import pandas as pd
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
