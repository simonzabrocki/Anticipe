import os
import glob
import pandas as pd
from convert_to_xlsx import convert_to_xlsx_file

def combine_files():
    cwd = os.path.abspath('')+ '/data/'

    
    indicators = [ 'SM_E/' , 'SM_GM/' , 'SM_S/' , 'SM_UA/' ]
    all =[]
    df = pd.DataFrame()
    
    for indicator in indicators:
        path =cwd+indicator
        files = os.listdir(path)
        
        for file in files:
            if file.endswith('.xls'):
                print("Starting converting " , file)
                filenames = convert_to_xlsx_file( path , file)
                all.append(filenames)
        print("Done")
        
        # remove xls files
        files_in_dir = glob.iglob(path+'*.xls')
        for _file in files_in_dir:
            os.remove(_file)
            
        
def merge_into_one():
    cwd = os.path.abspath('')+ '/data/'
    indicators = [ 'SM_E/' ] # , 'SM_GM/' , 'SM_S/' , 'SM_UA/' ]
    
    dflist =[]
    df = pd.DataFrame()
    
    for indicator in indicators:
        path =cwd+indicator
        files = os.listdir(path)
    
        for file in files:
            
            filename_is = os.path.splitext(file)[0]
                       
            data = pd.read_excel(path+file, skiprows=1)
            dflist.append(data)
            
        Excelwriter = pd.ExcelWriter("data_efficiency indicator.xlsx")
        #We now loop process the list of dataframes
        for i, df in enumerate (dflist):
            df.to_excel(Excelwriter, sheet_name="sheet" + str(i+1),index=False)
        #And finally save the file
        Excelwriter.save()

merge_into_one()    
    
    
