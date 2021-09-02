import pandas as pd


# def process_ME1():
#     df = pd.read_csv("data/indicator/ME1/raw/ME1_GGGI.M.csv")
#     print(df.head)
#     return df

def preprocess():
    ME1_DMC = (
        pd.read_csv("data/indicator/ME1/raw/ME1.0_OECD.M.csv")
          .drop(columns=['INDICATOR', 'SUBJECT', 'MEASURE', 'FREQUENCY','Flag Codes'])
          .rename(columns={'LOCATION':'ISO', 'TIME':'Year'})
          .set_index(['ISO', 'Year'])['Value']
    )
    ME1_GDPC = (
        pd.read_csv('data/indicator/ME1/raw/ME1.1_WB.M.csv', index_col=['ISO', 'Year'])['Value']
    )
    
    df = ME1_DMC * 1e3 / ME1_GDPC
    
    return df.dropna().reset_index()



config = {'Variable': 'ME1',
              'function': preprocess,
              'Description': 'Total domestic material consumption (DMC) per unit of GDP',
              'Source': 'OECD _AND_ WorldBank',
              'URL': 'https://data.worldbank.org/indicator _AND_ https://www.oecd-ilibrary.org/environment/material-consumption/indicator/english_84971620-en#:~:text=Domestic%20material%20consumption%20(DMC)%20refers,minus%20material%20and%20products%20exported.'}