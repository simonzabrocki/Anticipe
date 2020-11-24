
import country_converter as coco
import pandas as pd
import numpy as np

COUNTRY_INFOS = pd.read_csv('index/country_infos/countries_info.csv', index_col=0)


def ISO_to_Country(ISOs):
    '''
    Convert ISOs vector to Country

    Parameters
    ----------
    ISOs: np.array
        An array/series of ISO codes
    '''

    return coco.CountryConverter().data.set_index('ISO3').loc[ISOs]['name_short'].values


def ISO_to_Continent(ISOs):
    '''
    Convert ISOs vector to Continent

    Parameters
    ----------
    ISOs: np.array
        An array/series of ISO codes
    '''
    return coco.CountryConverter().data.set_index('ISO3').loc[ISOs]['continent'].values


def ISO_to_Unregion(ISOs):
    '''
    Convert ISOs vector to UNregion

    Parameters
    ----------
    ISOs: np.array
        An array/series of ISO codes
    '''
    return coco.CountryConverter().data.set_index('ISO3').loc[ISOs]['UNregion'].values


def ISO_to_IncomeLevel(ISOs, COUNTRY_INFOS=COUNTRY_INFOS):
    '''
    Convert ISOs vector to IncomeLevel

    Parameters
    ----------
    ISOs: np.array
        An array/series of ISO codes
    '''
    df = COUNTRY_INFOS.set_index('id')
    IncomeLevel = df.loc[df.index.intersection(set(ISOs)), 'incomeLevel.value']
    return IncomeLevel


def ISO_to_Region(ISOs, COUNTRY_INFOS=COUNTRY_INFOS):
    '''
    Convert ISOs vector to Region

    Parameters
    ----------
    ISOs: np.array
        An array/series of ISO codes
    '''
    df = COUNTRY_INFOS.set_index('id')
    Region = df.loc[df.index.intersection(set(ISOs)), 'region.value']
    return Region


def add_All_ISOs(df):
    '''
    Add all existing ISOs to a dataframe with ISO columns
    Parameters
    ----------
    df: pd.DataFrame
        A DataFrame with an ISO column
    '''
    full_ISOs = coco.CountryConverter().data[['ISO3']].rename(columns={'ISO3': 'ISO'})
    return pd.merge(df, full_ISOs, left_on='ISO', right_on='ISO', how='right')


def ISO_to_Everything(df, add_all_ISO=True):
    '''
    Add all the information to a data frame with an ISO columns

    Parameters
    ----------
    df: pd.dataframe
        A dataframe with an ISO index
    add_all_ISO: bool
        Whether to complete the ISO columns with all the existing ISOs
    '''
    df = df.copy()
    if add_all_ISO:
        df = add_All_ISOs(df)
    df.set_index('ISO', inplace=True)
    df['Country'] = ISO_to_Country(df.index)
    df['Continent'] = ISO_to_Continent(df.index)
    df['UNregion'] = ISO_to_Unregion(df.index)
    df['IncomeLevel'] = ISO_to_IncomeLevel(df.index)
    df['Region'] = ISO_to_Region(df.index)
    return df


def geometric_mean(df, axis=1):
    return np.exp(np.log(df.prod(axis=axis)) / df.notna().sum(axis=axis))
