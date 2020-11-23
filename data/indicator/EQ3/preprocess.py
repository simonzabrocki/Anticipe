import pandas as pd


def process_EQ3():
    df = pd.read_csv("data/indicator/EQ3/raw/EQ3_WB.M.csv")

    df = df[[
        'iso3c', 'country_name', 'total_msw_total_msw_generated_tons_year',
        'population_population_number_of_people'
    ]]

    df['Year'] = 2018

    df['Value'] = df['total_msw_total_msw_generated_tons_year'] / df[
        'population_population_number_of_people']

    df = df.drop(columns=[
        'total_msw_total_msw_generated_tons_year',
        'population_population_number_of_people'
    ]).rename(columns={
        'iso3c': 'ISO',
        'country_name': 'Country',
    })

    return df
