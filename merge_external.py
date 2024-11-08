''' these are the paths I have on my directory, could be different for you '''
cpi_path = 'CPIAUCSL.csv'
tornado_path = 'tornados_new.csv'

'''
ASSUMPTIONS: 
Uses these links, if something changes this code will need to be redone:
- population: https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population
- state info: https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area
- state abvr: https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations
- CPI data is collected from STL FRED: https://fred.stlouisfed.org/series/CPIAUCSL
    - Uses standard formatting from that website as of 2024
- Tornado information collected from here: https://www.spc.noaa.gov/wcm/#data
    - Uses standard formatting from that website as of 2024

OUTPUT: pandas df
'''

def create_extra_info(tornado_path, cpi_path):
    import pandas as pd

    # gets CPI information
    # this can be elsewhere, its chill here though
    def create_cpi(path):
        # gets CPI data

        df_CPI = pd.read_csv(path)

        BASE_YEAR =  308.742
        df_CPI['CPI_Multiplier'] =  BASE_YEAR / df_CPI['CPIAUCSL'].astype(int)
        df_CPI['DATE'] = pd.to_datetime(df_CPI['DATE'])

        df_CPI['year'] = df_CPI['DATE'].dt.year
        df_CPI['month'] = df_CPI['DATE'].dt.month
        return df_CPI

    # creates dfs
    cpi = create_cpi(cpi_path)
    tornados = pd.read_csv(tornado_path)
    population = pd.read_html('https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_historical_population',\
                              match='Name')[3]


    # merges cpi and tornado dfs
    merged = pd.merge(tornados, cpi[['CPI_Multiplier', 'year', 'month']], left_on=['yr', 'mo'], right_on=['year', 'month'])


    # this attempts to approximate annual population levels
    popT = population.transpose()
    popT.columns = popT.iloc[0]
    popT = popT[1:]
    popT.index = popT.index.astype(int)
    popT['United States'] = popT['United States'].str[:-4]
    popT['United States'] = popT['United States'].str.replace(',', '')
    popT.drop('Northern Mariana Islands[ad]', axis=1, inplace=True)
    popT = popT.astype(int)

    popTr = popT.reindex(range(1950, 2024))
    popTi = popTr.interpolate(method='linear', limit_direction='both')
    popi = popTi.transpose()


    # gets state area info
    state = pd.read_html('https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_area',\
                         match='State / territory')[0]
    state_simple = pd.concat([state['State / territory'], state.xs('sq mi', axis=1, level=1)], axis=1)

    # gets state abbrevations
    names = pd.read_html('https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations',\
                       match='Name')[0]
    abv = pd.concat([names['Name'], names.xs('Unnamed: 3_level_1', axis=1, level=1)], axis=1)

    # combines state and abbrevations
    state_info = pd.merge(state_simple, abv, left_on='State / territory',\
                          right_on='Name', how='inner')
    state_info = state_info.drop('Name', axis=1).drop_duplicates()

    # steps to help make the merge easy
    popi2 = pd.merge(popi, abv, left_index=True, right_on='Name')
    test = pd.melt(popi2, id_vars='ANSI')
    test.rename(columns={'value': 'pop'}, inplace=True)

    # merged
    cool_tornado = pd.merge(merged, test, left_on=['yr','st'], right_on=['variable','ANSI'], how='left')

    # final merge.  All information is now present, redundant columns are dropped
    complete = pd.merge(cool_tornado, state_info, on='ANSI')
    complete.drop(['variable', 'State / territory', 'year', 'month', 'ANSI'], axis=1, inplace=True)

    # add in USA regions
    # not going to update above code, just going to add more here below
    region_path = 'https://raw.githubusercontent.com/cphalpert/census-regions/refs/heads/master/us%20census%20bureau%20regions%20and%20divisions.csv'
    region_df = pd.read_csv(region_path)
    complete = pd.merge(complete, region_df, left_on='st', right_on='State Code', how='left')
    
    return complete

'''
Could this have been separate functions?  Sure.  If I did this again I'd probably modularize it more
HOWEVER
Don't fix what isn't broke.  This was copied over from .ipynb file.  It works for scope of project.
'''
