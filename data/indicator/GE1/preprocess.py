def process_GE1_0(df):
    df = df.copy()
    df['Description'] = df['gas'] + ' ' + df['sector'] + ' Tons'
    df['Value'] = df['Value'] * 1e6

    return df[df['Value'] > 0].drop(columns=['sector', 'gas', 'unit'])
