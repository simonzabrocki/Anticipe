import os
import pandas as pd
import pandas as pd
from bs4 import BeautifulSoup

def convert_to_xlsx(file):
    
    filename_is = os.path.splitext(file)[0]
    
    with open(file) as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'xml')
        writer = pd.ExcelWriter(filename_is+'.xlsx')
        for sheet in soup.findAll('Worksheet'):
            sheet_as_list = []
            for row in sheet.findAll('Row'):
                sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in row.findAll('Cell')])
            pd.DataFrame(sheet_as_list).to_excel(writer, sheet_name=sheet.attrs['ss:Name'], index=False, header=False)
        writer.save()
        return filename_is

def combine_files():
    
    
    
    
    
    
    dataFileUrl = "Container port traffic (TEU 20 foot equivalent units, thousands).xls"
    filename = convert_to_xlsx(dataFileUrl)
    data = pd.read_excel(filename+".xlsx" , skiprows=1)
    
    print(data.head(5))
    
    
    
    """
    df = pd.read_excel("Container port traffic (TEU 20 foot equivalent units, thousands).xls" , engine=None)
    print(df.head(10))
    """
    """
    cwd = os.path.abspath('')
    indicators = [ '/test']# , '/SM_E' , '/SM_GM' , '/SM_S' , '/SM_UA' ]
    df = pd.DataFrame()
    for indicator in indicators:
        url =cwd+indicator
        files = os.listdir(url)
        for file in files:
            print(file)
            if file.endswith('.xls'):
                print(file)
    
    df = pd.ExcelFile(r"Container port traffic (TEU 20 foot equivalent units, thousands).xls" , engine="openpyxl")
    print(df.head(10))
    
        df.to_excel('total_sales.xlsx')
        print("++++++++++++++++++++++++++")
        
        
    
    
            df = df.append(pd.read_excel(file), ignore_index=True)
    #df.head()
    """
combine_files()

