import itertools
import pandas as pd
import math


def create_full_index(df):
    ISOs = df['ISO'].unique().tolist()
    min_year = min(2000, df.Year.min())
    max_year = 2020 + 1
    Years = list(range(min_year, max_year))
    full_index = pd.DataFrame(list(itertools.product(*[ISOs, Years])), columns=['ISO', 'Year'])
    return full_index


def create_missing_value_df(df):
    df = df.copy()
    full_index = create_full_index(df)
    df = pd.merge(df, full_index, on=['ISO', 'Year'], how='right')
    non_imputed = ['Description', 'Variable', 'From', 'Source', 'URL']
    df[non_imputed] = df[non_imputed].apply(lambda x: x.fillna(x.value_counts().index[0]))
    df['Imputed'] = df['Value'].apply(lambda x: math.isnan(x))
    return df.sort_values(by=['ISO', 'Year'])


def impute_data_using_rule(df, interpolation_rule):
    df = df.copy()
    df = create_missing_value_df(df)

    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df = df.set_index('Year')

    imputed_values = df.groupby('ISO').apply(lambda group: interpolation_rule(group))

    imputed_values = imputed_values.reset_index().melt(
        id_vars=['ISO']).sort_values(by=['ISO', 'Year'])
    imputed_values = imputed_values.rename(columns={'value': 'Imputed_Value'})

    result = pd.merge(df.reset_index(), imputed_values, on=['ISO', 'Year'])
    result = result.drop(columns=['Value']).rename(columns={'Imputed_Value': 'Value'})
    result['Year'] = result['Year'].dt.year
    return result


def interpolate_linear(df):
    def step_1(x):
        return x.interpolate(method='linear', limit=5, limit_direction='both')

    def step_2(x):
        return x  # .interpolate(method='bfill', limit=1)

    def step_3(x):
        return x  # .interpolate(method='ffill', limit=1)

    return step_3(step_2(step_1(df['Value'])))


def interpolation_rule_SL1(df):
    def step_1(x):
        return x.interpolate(method='bfill', limit=20)

    def step_2(x):
        return x  # .interpolate(method='bfill', limit=1)

    def step_3(x):
        return x.interpolate(method='ffill', limit=20)

    return step_3(step_2(step_1(df['Value'])))
