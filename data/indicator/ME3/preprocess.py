import pandas as pd
from processing.utils import add_ISO


# def preprocess():
#     df = (
#         pd.read_csv('data/indicator/ME3/raw/ME3_FAO.M.csv')
#           .groupby(['Area', 'Year', 'Element'])['Value'].sum().reset_index()
#           .pivot(index=['Area', 'Year'], columns='Element', values='Value')
#     )
    
#     df['Value'] = df['Loss'] / df['Production'] * 100
#     return df['Value'].reset_index().rename(columns={'Area': 'Country'})



# config =  {'Variable': 'ME3',
#               'function': preprocess,
#               'Description': 'Share food loss to total food production (Percent)',
#               'Source': 'FAO',
#               'URL': 'http://www.fao.org/faostat/en/#data/SCL'
#               }



def preprocess_loss():
    df = (
        pd.read_csv('data/indicator/ME3/raw/ME3_FAO.M.csv')
          .groupby(['Area', 'Year', 'Element'])['Value'].sum().reset_index()
          .pivot(index=['Area', 'Year'], columns='Element', values='Value')
    )
    
    df['Value'] = df['Loss'] / df['Production'] * 100
    df = df['Value'].reset_index().rename(columns={'Area': 'Country'})
    
    df = add_ISO(df)
    return df


def preprocess_waste():
    cons = (
        pd.read_csv('data/indicator/ME3/raw/ME3.0_FAO.M.csv')
          .groupby(['Area', 'Year'])['Value']
          .sum().to_frame(name='Value')     
          .reset_index()
          .rename(columns={'Area': 'Country'})
    )
    cons = add_ISO(cons)
    
    waste = (
        pd.read_csv('data/indicator/ME3/raw/ME3.1_SDG.M.csv')
          .query("GeoAreaName not in ['Southern Africa']")
          .groupby(['GeoAreaName', 'TimePeriod'])['Value']
          .sum().reset_index()
          .rename(columns={'GeoAreaName': 'Country', 'TimePeriod': 'Year'})
          .drop(columns=['Year'])
    
    )
    waste = add_ISO(waste)
    
    df = pd.merge(cons, waste, on=['ISO'], suffixes=('_cons', '_waste'))
    
    df['Value'] = df['Value_waste'] / df['Value_cons'] * 100
    return df[['ISO', 'Year', 'Value']]


def preprocess():
    df_waste = preprocess_waste()
    df_loss = preprocess_loss()
    
    df = df_loss.merge(df_waste, on=['ISO', 'Year'], suffixes=('_loss_to_production', '_waste_to_consumption'))
    
    df['Value'] = df[['Value_loss_to_production', 'Value_waste_to_consumption']].mean(axis=1)
    
    
    #ST = pd.DataFrame({"Indicator": ['ME3'], "Number of targets": 1, "Relation": 'negative', 'Target 1': 0, 'Target 2': np.nan}).set_index('Indicator')
    #df.rename(columns={"Value": 'ME3'}).groupby(['Year']).apply(lambda x: GreenGrowthScaler().normalize(x[['ME3', 'ISO']], ST)).reset_index().drop(columns=['level_1']).rename(columns='')
    
    return df[['ISO', 'Year', 'Value']]
    


config =  {'Variable': 'ME3',
              'function': preprocess,
              'Description': 'Average of food loss to production and food waste to consumption',
              'Source': 'FAO',
              'URL': 'http://www.fao.org/faostat/en/#data/SCL'
              }