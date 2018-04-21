
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[36]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    with open('university_towns.txt') as f:

        x=f.readlines()

    state_region = []
    curr_state=''

    for line in x:
        line = line.strip()
        if line[-6:] == '[edit]':
                curr_state = line[:-6]
        elif '(' in line:
                region = line[:line.index('(')-1]
                state_region.append([curr_state, region])
        else:
            region = line
            state_region.append([curr_state,region])
    df = pd.DataFrame(state_region, columns=["State", "RegionName"])
    
    return df


# In[90]:

#get_list_of_university_towns().head()


# In[69]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp_df = pd.read_excel('gdplev.xls', skiprows = 219)
    gdp_df = gdp_df[['1999q4', 12323.3]]
    gdp_df.columns = ['Quarter', 'GDP']
    for index in range(2, len(gdp_df)):
        if (gdp_df.iloc[index - 2, 1] > gdp_df.iloc[index - 1, 1]) and (gdp_df.iloc[index - 1, 1] > gdp_df.iloc[index, 1]):
            return gdp_df.iloc[index - 1, 0]
    return None


# In[70]:

#get_recession_start()


# In[85]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp_df = pd.read_excel('gdplev.xls', skiprows = 219)
    gdp_df = gdp_df[['1999q4', 12323.3]]
    gdp_df.columns = ['Quarter', 'GDP']
    
    # store the start of recession
    recession_start = get_recession_start()
    # identify the index of that quarter in df
    start = gdp_df[gdp_df['Quarter'] == recession_start].index.tolist()[0]
    # consider the df starting from recession
    gdp_df = gdp_df.iloc[start : ]
    
    # now check for recession end
    for index in range(2, len(gdp_df['Quarter'])):
        if (gdp_df.iloc[index - 2, 1] < gdp_df.iloc[index - 1, 1]) and (gdp_df.iloc[index - 1, 1] < gdp_df.iloc[index, 1]):
            return gdp_df.iloc[index, 0]
    return None


# In[86]:

#get_recession_end()


# In[88]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    # again same, read the exel file
    gdp_df = pd.read_excel('gdplev.xls', skiprows = 219)
    gdp_df = gdp_df[['1999q4', 12323.3]]
    gdp_df.columns = ['Quarter', 'GDP']
    
    # store the start of recession
    recession_start = get_recession_start()
    recession_start_index = gdp_df[gdp_df['Quarter'] == recession_start].index.tolist()[0]
    # store end of recession
    recession_end = get_recession_end()
    recession_end_index = gdp_df[gdp_df['Quarter'] == recession_end].index.tolist()[0]
    
    # consider the recession period only
    gdp_df = gdp_df.iloc[recession_start_index : recession_end_index + 1]
    
    recession_bottom_quarter = None
    recession_bottom_gdp = None
    for index in range(len(gdp_df)):
        if recession_bottom_quarter == None:
            recession_bottom_quarter, recession_bottom_gdp = gdp_df.iloc[index, 0], gdp_df.iloc[index, 1]
        
        elif recession_bottom_gdp > gdp_df.iloc[index, 1]:
            recession_bottom_quarter, recession_bottom_gdp = gdp_df.iloc[index, 0], gdp_df.iloc[index, 1]
        
    return recession_bottom_quarter


# In[89]:

#get_recession_bottom()


# In[130]:


'''
def convert_housing_data_to_quarters():
    Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    #df = pd.read_csv('City_Zhvi_AllHomes.csv')
    
    # drop unneccessery columns
    #df.drop(['RegionID', 'Metro', 'CountyName', 'SizeRank'], axis = 1, inplace = True)
    #cols = list(df.columns)
    #df.drop(cols[2:47], axis = 1, inplace = True)
    
    #df['State'] = df['State'].map(states)
    
   # yrs = list(range(2000, 2017))
    #qtr = ['q1', 'q2', 'q3', 'q4']
    #new_cols = [str(yr)+ q for yr in yrs for q in qtr]
    
    #cols = list(df.columns)
    #convert_qarter = 2
    #for i in new_cols:
     #   df[i] = np.mean()
    #return df
    
def new_col_names():
    #generating the new coloumns names 
    years = list(range(2000,2017))
    quars = ['q1','q2','q3','q4']
    quar_years = []
    for i in years:
        for x in quars:
            quar_years.append((str(i)+x))
    return quar_years[:67]
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data.drop(['Metro','CountyName','RegionID','SizeRank'],axis=1,inplace=True)
    data['State'] = data['State'].map(states)
    data.set_index(['State','RegionName'],inplace=True)
    col = list(data.columns)
    col = col[0:45]
    data.drop(col,axis=1,inplace= True)

    #qs is the quarters of the year
    qs = [list(data.columns)[x:x+3] for x in range(0, len(list(data.columns)), 3)]
    
    # new columns
    column_names = new_col_names()
    for col,q in zip(column_names,qs):
        data[col] = data[q].mean(axis=1)
        
    data = data[column_names]
    return data


# In[131]:


#convert_housing_data_to_quarters()


# In[132]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters().copy()
    data = data.loc[:,'2008q3':'2009q2']
    data = data.reset_index()
    def price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
    data['up&down'] = data.apply(price_ratio,axis=1)
    #uni data 
    
    uni_town = get_list_of_university_towns()['RegionName']
    uni_town = set(uni_town)

    def is_uni_town(row):
        #check if the town is a university towns or not.
        if row['RegionName'] in uni_town:
            return 1
        else:
            return 0
    data['is_uni'] = data.apply(is_uni_town,axis=1)
    
    
    not_uni = data[data['is_uni']==0].loc[:,'up&down'].dropna()
    is_uni  = data[data['is_uni']==1].loc[:,'up&down'].dropna()
    def better():
        if not_uni.mean() < is_uni.mean():
            return 'non-university town'
        else:
            return 'university town'
    p_val = list(ttest_ind(not_uni, is_uni))[1]
    #p_val = ttest_ind(not_uni, is_uni)
    different = True if p_val < 0.01 else False
    result = (different, p_val, better())
    return result


# In[133]:

print(run_ttest())


# In[ ]:



