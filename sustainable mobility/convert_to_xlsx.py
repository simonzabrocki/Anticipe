import pandas as pd
from bs4 import BeautifulSoup
import os

def convert_to_xlsx_file(path , file):
    filename_is = os.path.splitext(file)[0]
    url = path+filename_is+'.xls'
    
    with open(url) as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'xml')
        
        writer = pd.ExcelWriter(path+filename_is+'.xlsx')
        for sheet in soup.findAll('Worksheet'):
            sheet_as_list = []
            for row in sheet.findAll('Row'):
                sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in row.findAll('Cell')])
            pd.DataFrame(sheet_as_list).to_excel(writer, sheet_name=sheet.attrs['ss:Name'], index=False, header=False)
        writer.save()
        return filename_is