def answer_two():
    # just copy & paste above function
    # outer join three df to get total row count
    
    # --------------  Energy -----------------------
    # skip header and footer information
    energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, 
                           skip_footer = 38)
    
    
    # assigning columns name
    energy.columns = ['Unnamed','Country', 'Country_1','Energy Supply', 'Energy Supply per Capita', '% Renewable']
    # drop replicated 'country' column and replacing '...' unavailable values with np.NaN
    energy = energy.drop(['Unnamed','Country_1'], axis = 1).replace('...', np.NaN)
    # modifying Energy Supply from peta to giga joules
    energy['Energy Supply'] *= 1000000
    # set 'Country' as index
    energy = energy.reset_index()
    energy = energy.set_index('Country').drop('index', axis = 1)
    
    # changing index values --->
    table = {"Republic of Korea": "South Korea",
             "United States of America": "United States",
             "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
             "China, Hong Kong Special Administrative Region": "Hong Kong"}
    energy_index = energy.index
    for cntry in energy_index:
        if cntry in table:continue
        if '(' in cntry:
            name = cntry[:cntry.find('(') - 1]
            table[cntry] = name
        elif cntry.isalnum():
            name = ''.join([ch for ch in cntry if cntry.isalpha()])
            table[cntry] = name
        else:table[cntry] = cntry
    energy = energy.rename(index = table)
    
    
    # ------------------ world bank GDP -----------------
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    idx_rename = {"Korea, Rep.": "South Korea", 
                  "Iran, Islamic Rep.": "Iran",
                  "Hong Kong SAR, China": "Hong Kong"
                 }
    GDP = GDP.rename(columns = {'Country Name': 'Country'})
    GDP = GDP.reset_index()
    GDP = GDP.set_index('Country').drop('index', axis = 1)
    GDP = GDP.rename(index = idx_rename)
    
    # -----------------  Sciamgo Journal ----------------
    ScimEn = pd.read_excel('scimagojr-3.xlsx', index_col = 1)
    ScimEn = ScimEn.reset_index()
    ScimEn = ScimEn.set_index('Country')
    
    # --------------------- merging dataframes ---------------
    yrs = list(map(str, range(2006, 2016)))
    
    first_merge = pd.merge(GDP, energy, how = 'outer', left_index = True, right_index = True)
    
    df = pd.merge(ScimEn, first_merge, how = 'outer', left_index = True, right_index = True)
    y = len(df.index)
    #df = (pd.merge(GDP, ScimEn, how = 'outer', left_index = True, right_index = True))
    
    #df = pd.merge(df, energy, how = 'outer', left_index = True, right_index = True)
    #total_row_count = len(df.index)
    #loss_value = total_row_count - 15
    #return loss_value
    x = set()
    for i in energy.index:
        x.add(i)
    for i in GDP.index:
        x.add(i)
    for i in ScimEn.index:
        x.add(i)
    
    
    return df.shape

answer_two()
