'''
This file includes the matric calculation fuinctions used to chose the requiered sector
out of the final demand table (Y), and find the total output (X) and its emissions (CS)(X).
'''

## Upload libraries
import sys
import pandas as pd
import numpy as np
# export file path:
expath = 'C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/HY_IO_const_CA/csv_exports/'


def vector_X ( tables_L, vector_Y):
    """
    This function calculates a total output vextor from a given final demand vector x = (L)(Y)
    It returns vector X and diagonolized vextor X
    the vector is then diagonolised into a 16Kx16K martix to preserve commodity distribution details 
    """
    vector_X = tables_L.dot(vector_Y)
    #
    vector_X_diag = pd.DataFrame(np.diag(vector_X.sum(1)), index=vector_X.index, columns= vector_X.index)
    return (vector_X, vector_X_diag)

def env_impact(tables_CS, vector_X_diag):
    """This function calculates the environmental total output vector_env=(CS)(X)
    and sorts for short term CO2e (100yr)
    Diagnolised X (vector_X_diag) multiplication provides detailed breakwon commodities
    and theier country of origin.
    
    """
    vector_env = tables_CS.dot(vector_X_diag)

    co2e_impact = vector_env.loc[('Climate change, short term','kg CO2 eq (short)')].sort_values(ascending=False)
    
    return co2e_impact

def vector_D(tables_A, vector_Y):
    """
    This function calculates a total output vextor from a given final demand vector D = (A)(Y)
    It returns vector X and diagonolized vextor X
    the vector is then diagonolised into a 16Kx16K martix to preserve commodity distribution details 
    """
    vector_D = tables_A.dot(vector_Y)
    #
    vector_D_diag = pd.DataFrame(np.diag(vector_D.sum(1)), index=vector_D.index, columns= vector_D.index)
    return (vector_D, vector_D_diag)


#HY CIRAIG CALC
def sector(province, sector):
    '''1. This function defines the province and sector (Gross fixed capital formation) 
    sector = ('CA-ON','Gross fixed capital formation, Construction')'''
    sector = (province, sector)
    return sector


##HY
def diagnolize(sector, tables_Y):
    """
    # 2. This function diagonalizes the demand
    """
    diag_Y = pd.DataFrame(np.diag(tables_Y.loc[:, sector].sum(1)),
                                                index=tables_Y.index, columns=tables_Y.index)
    return diag_Y

##HY
def contribution(tablesC, tablesS, tablesL, diag_Y):
    """"
    3. this function calculates the contribution analysis (emissions of the final demand vector):
    """
    contribution_analysis = tablesC.dot(tablesS).dot(tablesL).dot(diag_Y)
    return contribution_analysis

## HY

def dir_emissions(tables_C , tables_FY, commodities, province, contribution_analysis):
    """
    4. This function is not requiered in construction emission calculation (relates to operational emissions of the sector - e.g. gas and elec in houshold expenditures)
    this function adds direct emissions seperately. Also we reformat them a bit.
    """    
    direct_emissions = tables_C.dot(tables_FY)[tables_C.dot(tables_FY)!=0].dropna(how='all',axis=1).fillna(0)
    direct_emissions.columns = direct_emissions.columns.droplevel(1)
    direct_emissions.columns = pd.MultiIndex.from_product([direct_emissions.columns.levels[0], 
    commodities])

    contribution_analysis = pd.concat([contribution_analysis, 
                                                  direct_emissions.drop([
                                                      i for i in direct_emissions.columns.levels[0] if i != province],axis=1)],
                                                 axis=1)
    return contribution_analysis

##HY
def short_term_emissions(contribution_analysis):
    """
    5. This function calculates short term emissions (focus on GWP100)
    """
    contribution_analysis = contribution_analysis.loc[('Climate change, short term','kg CO2 eq (short)')].T.sort_values(ascending=False)
    return contribution_analysis


# These functions calculates the total environmental impact of a chosen final demand vector (vector_Y) 
# The level of analysis is by tables_Y  headar hierarchy: 1.Canada, 2.Province, 3.Sector, 4.Industry.
# in this function  - short term CO2e are calculated and arranged in assending order.
# the matrix multiplication order is C(33X11K)*S(11KX16K)
        #CS(33X16K)*L(16Kx16K)
            #CSL(11X16K)*Y(16Kx 1) - 1 sum of table_Y rows.
# The 16K (in all tables) represent commoidties
# the Y columns represent industries/sectors.
# All final demand of commodities (rows) are summed - therefore, this function calculates one Y vector Canada, Province, Industry Level) 
# the Y table is a rectangular commodity by industry table.


# To recieve an impact report, assign a final demand vector Y and load all tables. 
# for direct emissions, multiply and append FY table with Y vector. See dir_emmission() function cell below.  

##Slice a final demand vector

def final_demand_sector(sector= [('CA-ON', 'Gross fixed capital formation', 'Construction','Residential structures')]):
    '''Slice a final demand vector
    '''
    vector_Y = tables_Y[sector]
    return vector_Y


##Commodity Isolation (row) function
def isolate_commodity_to_Y_vector(province = 'CA-ON', commodity = 'Residential buildings'):
    '''this function isolates commodity by province, sums it up and turnes it into a series.
    The function replaces all other vector-commodities with 0 so that when it runs on the model 
    we only calculate the commodity impact. '''
    #Isolate Province
    df = tables_Y[province]             #final demand of province
    sum_Y = pd.DataFrame(df).sum(1)     #sums commodity rows
    sum_Y
    #create a 0 sum vector (with Y table rows)
    sum_Y_null = pd.Series(0, index=sum_Y.index)
    #isolate chosen commodity summary 
    sum_Y_null.loc[(province, commodity)] = sum_Y.loc[(province, commodity)]
    sum_Y_null.sum()
    return sum_Y_null


def total_co2e(vector_Y, tables_C , tables_S , tables_L ):
    ''' This func findes the CO2e of a selected Y dataframe '''
    ## HY This diagnolizes the Y (final demand vector)
    Y_diag = pd.DataFrame(np.diag(vector_Y.sum(1)),
                                    index=vector_Y.index, columns=vector_Y.index)
    Y_diag
    ## This line calculates the total output enmissions
    total_output = tables_C.dot(tables_S).dot(tables_L).dot(Y_diag)
    total_output
    ## This lin sorts out the short term impacts of the selected data
    report = total_output.loc[('Climate change, short term','kg CO2 eq (short)')].T.sort_values(ascending=False)
    return report


def total_co2e_series(vector_Y):
    '''#total_co2e_series is a function that isolates each commodity in from the Y table
    and runs just that commodity on the model - This can be used to identiy 
    emission impacts of specific commodities like Steel, Wood or vegtables.'''
    #multiply chosen commodity vector and retreve impact
    # 2. Calculating encironemtnal impact using CIRIAGS's IO tables
    Y_diag = pd.DataFrame(np.diag(vector_Y),
                        index=vector_Y.index, columns=vector_Y.index)
    Y_diag

    total_output = tables_C.dot(tables_S).dot(tables_L).dot(Y_diag)
    total_output
    ## This lin sorts out the short term impacts of the selected data
    report = total_output.loc[('Climate change, short term','kg CO2 eq (short)')].T.sort_values(ascending=False)
    return report


def join_material_index(
        commod_LCA_df, 
        path ='C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/CA_Const_EEIO/Data/lists/'):
    
    '''This function adds a material index to the generated L(AY) commodity df
    (blue). Returnes [0]- material df and LCA classification
    [1] - emission typy,
    [2] - includes commodity breakdown)
    '''

    # # 1. import calssification
    path = 'C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/CA_Const_EEIO/Data/lists/'
    class_list = pd.read_csv(path +  'material_lca_classification09.csv')
    # arrange by country/commodity
    class_list.set_index(['country_province','commodity' ])
    
    # removes multi-index from LCA DF     left = on_res_commod_LCA.droplevel([1], axis = 1)
    left = commod_LCA_df.droplevel([1], axis = 1)
    #Creating a refernce index for both DF (country+commodity)
    left = left.reset_index()
    left['new_index'] = left['level_0'] + ' ' + left['level_1']
    left = left.set_index('new_index')
    left

    right = class_list
    right['new_index'] = right['country_province'] + ' ' + right['commodity']
    right = right.set_index('new_index')
    right

    #Joining DF
    material_df = left.join(right)
    material_df

    #Sorts by material lev 1 lev 2
    material_df_sum = material_df.groupby((['lev1_name', 'lev2_name',])).sum().drop('lev1', axis =1 )
    material_df_commod = material_df.groupby((['lev1_name', 'lev2_name', 'commodity'])).sum().drop('lev1', axis =1 )

    return [material_df, material_df_sum, material_df_commod]



def attach_mat_class(emission_df):
    '''This function attaches the material classificaiton to a chosen enission df
    - updated emission classificaiton is material_lca_classification09.csv '''

    # # 1. import calssification
    path = 'C:/Users/Hatzav/OneDrive - University of Toronto/HY_UofT/002CarbonBudgeting/Code/CA_Const_EEIO/Data/lists/'
    class_list = pd.read_csv(path + 'material_lca_classification09.csv')
    # arrange by country/commodity
    class_list.set_index(['country_province', 'commodity' ])

    # removes multi-index from LCA DF     left = on_res_commod_LCA.droplevel([1], axis = 1)
    left = emission_df
    #Creating a refernce index for both DF (country+commodity)
    left = left.reset_index()
    left['new_index'] = left['Unnamed: 0'] + ' ' + left['Unnamed: 1']
    left = left.set_index('new_index')
    left

    right = class_list
    right['new_index'] = right['country_province'] + ' ' + right['commodity']
    right = right.set_index('new_index')
    right

    #Joining DF
    material_df = left.join(right)
    return material_df
