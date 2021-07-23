from hampel import hampel


def filter_outliers_from_ISO(df):
    ts = hampel(df['Value'].reset_index(drop=True), window_size=3, n=1, imputation=True).values
    df.loc[:, 'filtered_Value'] = ts
    df['Corrected'] = abs(df['filtered_Value'] - df['Value']) > 1e-3
    return df


def filter_outliers(df):
    df = df.groupby('ISO').apply(lambda group: filter_outliers_from_ISO(group))
    df = df.drop(columns=['Value']).rename(columns={'filtered_Value': 'Value'})
    return df
