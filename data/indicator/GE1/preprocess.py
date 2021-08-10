# def process_GE1_0(df):
#     df = df.copy()
#     df['Description'] = df['gas'] + ' ' + df['sector'] + ' Tons' # + ' MtCO2eq
#     df['Value'] = df['Value'] * 1e6

#     return df[df['Value'] > 0].drop(columns=['sector', 'gas', 'unit'])

def process_GE1_0(df):
    df = df.copy()
    piv = df.pivot(index=['ISO', 'Year'], columns=['sector'], values='Value')
    piv['Value'] = (piv['Total excluding LUCF'] - piv['Agriculture']) * 1e6
    piv = (
        piv['Value'].reset_index().assign(Description='C02 Total excluding LUCF and Agriculture Tons')
                    .assign(Source='CAIT _AND_ PIK')
    )
    
    
    return piv.query('Value > 0')