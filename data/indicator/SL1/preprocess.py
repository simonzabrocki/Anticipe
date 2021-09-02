import pandas as pd

#
# def process_SL1():
#
#     df = pd.read_csv('data/indicator/SL1/raw/SL1_GGGI.M.csv', index_col=0)
#     df = df.rename(columns={'SL1_GGGI': 'Value'})
#
#     return df



def preprocess():
    df = pd.read_csv('data/indicator/SL1/raw/SL1_FAO.M.csv').query("Element == 'Cropland nutrient flow per unit area'")
    df = df.drop(columns=['Domain', 'Domain Code', 'Area Code (FAO)', 'Element Code',
                          'Item Code', 'Year Code', 'Flag', 'Flag Description', 'Unit', 'Element'])
    
    pivoted = df.pivot(index=['Area', 'Year'], columns='Item', values='Value')#.fillna(0)

    NB = pivoted['Synthetic Fertilizers'] \
        + pivoted['Manure applied to Soils'] \
        + pivoted['Atmospheric Deposition'] \
        + pivoted['Biological Fixation'] \
        - pivoted['Crop Removal']

    NB = NB.reset_index()
    NB.columns = ['Country', 'Year', 'Value']
    NB['Value'] = abs(NB['Value'])

    
    NB[NB['Value'] < 0] = 5 - NB[NB['Value'] < 0]  # mirror ???
    return NB


config = {'Variable': 'SL1',
             'function': preprocess,
             'Description': 'Nutrient balance per unit area',
             'Source': 'FAO',
             'URL': 'http://fenix.fao.org/faostat/internal/en/#data/ESB'}

# def process_SL1():

#     df = pd.read_csv('data/indicator/SL1/raw/SL1_FAO.M.csv')
#     df = df.rename(columns={'Area': 'Country'})
#     # df['Value'] = abs(df['Value'])
#     df[df['Value'] < 0] = 5 - df[df['Value'] < 0]  # mirror
#     return df[['Country', 'Year', 'Value']]
