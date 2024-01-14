import sys
import pandas as pd
import numpy as np
# export file path:
expath = 'C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/HY_IO_const_CA/csv_exports/'


##
def machine_loc(file_name,index_colf = [0,1], headerf = [0,1,2]):
    '''
    Uploads table file either from laptop or VM
    Tables name eg: tables_Y (final demad) 
    file name: csv file name in folder
    Notice, CSV are multi-index, ther exceed size limit unless column and row indexes are determines (index_cold, and headarf)
    '''
    expath_vm = 'C:/Users/yoffehat/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/HY_IO_const_CA/CIRAIG_tables/'
    #laptop file location
    expath_laptop = 'C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/HY_IO_const_CA/CIRAIG_tables/'

    try:
        path = expath_vm
        tables = pd.read_csv(path + file_name, index_col = index_colf, header = headerf)
        print ('loading '+ file_name + ' files on VM')
        print (file_name + ' loaded successfuly')
        return tables
    
    except:
        path = expath_laptop
        print ('Couldnt load file on VM')
        print ('loading '+ file_name + ' from hard drive...')
        tables = pd.read_csv(path + file_name, index_col = index_colf, header = headerf)
        print (file_name + ' loaded successfuly')
        return tables 