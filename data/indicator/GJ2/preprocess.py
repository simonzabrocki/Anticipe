import pandas as pd

def preprocess():
    df = (
        pd.read_excel('data/indicator/GJ2/raw/IRENA_RE_Jobs_Annual_Review_2020.M.xlsx')
          .rename(columns={'Country/area': 'Country', 'Jobs (thousand)': 'Value'})
          .query("Technology == 'All technologies'")
          .drop(columns=['Source', 'Note', 'Technology'])
    )
    
    return df


config =  {'Variable': 'GJ2',
              'function': preprocess,
              'Description': 'Employment in renewable energy ',
              'Source': 'IRENA',
              'URL': 'https://www.irena.org/-/media/files/IRENA/Agency/Publication/2020/Sep/IRENA_RE_Jobs_2020.pdf'}