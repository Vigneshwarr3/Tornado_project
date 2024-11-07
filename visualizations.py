'''
This can host all of the visualizations as functions that we need for the website
Whenever we want to display a vis, we can just call the function and input the correct parameters
Everything should be fairy self explanatory
'''

'''
These obviously can be edited for design, titles, and to be able to print properly on the app
This just gets the framework.  We can add the details in as desired or needed

KNOWN FEATURES TO ADD OR EDIT
- Titles and axis
- Themes and color schemes
- iloc[] => some are 1:10, we can adjust as we feel is appropriate
    - maybe this means we put a limit on how many states can be selected?
    - if someone wants to select more than 10 states or so, we can think about
        how we would want to approach that for UX

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

''' INFLATION ADJUSTED LOSSES '''

# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def infl_adj_loss_state(df, states, years):
    df['loss_adjusted'] = df['damage'] * df['CPI_Multiplier']
    new_df = df[df['st'].isin(states)]
    new_df = new_df[df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby('st')['loss_adjusted'].sum().reset_index()
    
    sns.barplot(data = group_df.iloc[0:10], x = 'st', y = 'loss_adjusted')
    plt.title(f"Inflation adjusted loss for states in the years {years[0]} - {years[1]}")
    plt.xlabel("state")
    plt.ylabel("dollar loss, inflation adjusted for 8/24")               
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def infl_adj_loss_state_year(df3, states, years):    
    df3['loss_adjusted'] = df3['damage'] * df3['CPI_Multiplier']
    new_df = df3[df3['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),
                                                 int(years[1])) )) ]
    group_df = new_df.groupby(['st', 'yr'])['loss_adjusted'].sum().reset_index()
    sns.lineplot(data=group_df, x='yr', y='loss_adjusted', hue='st', marker='o')
    #plt.title(f"Inflation adjusted loss for states in the years {years[0]} - {years[1]}")
    plt.xlabel("year")
    plt.ylabel("dollar loss, inflation adjusted for 8/24")
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end] 
def infl_adj_loss_state_per10ksqmi(df, states, years):
    df['loss_adjusted'] = df['damage'] * df['CPI_Multiplier']
    df['loss_per_area'] = df['loss_adjusted'] / df['Total area'] * 10000
    new_df = df[df['st'].isin(states)]
    new_df = new_df[df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby('st')['loss_per_area'].sum().reset_index()
    
    
    sns.barplot(data = group_df.iloc[0:10], x = 'st', y = 'loss_per_area')
    plt.title(f"Inflation adjusted loss for states in the years {years[0]} - {years[1]}")
    plt.xlabel("state")
    plt.ylabel("dollar loss per 10k sq mi, inflation adjusted for 8/24") 
    
    
''' FATALITIES '''

# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def fat_state(df, states, years):
    new_df = df[df['st'].isin(states)]
    new_df = new_df[df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby('st')['fat'].sum().reset_index()
    
    
    sns.barplot(data = group_df.iloc[0:10], x = 'st', y = 'fat')
    plt.title(f"Fatalities for states in the years {years[0]} - {years[1]}")
    plt.xlabel("state")
    plt.ylabel("fatalities") 
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def fat_state_10ksqmi(df, states, years):
    df['fat_per_area'] = df['fat'] / df['Total area'] * 10000
    new_df = df[df['st'].isin(states)]
    new_df = new_df[df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby('st')['fat_per_area'].sum().reset_index()
    
    sns.barplot(data = group_df.iloc[0:10], x = 'st', y = 'fat_per_area')
    plt.title(f"Fatalitiess for states in the years {years[0]} - {years[1]}")
    plt.xlabel("state")
    plt.ylabel("fatalities per 10k sq mi") 
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def fat_state_10kppl(df, states, years):
    df['fat_per_ppl'] = df['fat'] / df['pop'] * 10000
    new_df = df[df['st'].isin(states)]
    new_df = new_df[df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby('st')['fat_per_ppl'].sum().reset_index()
    
    
    sns.barplot(data = group_df.iloc[0:10], x = 'st', y = 'fat_per_ppl')
    plt.title(f"Fatalities for states in the years {years[0]} - {years[1]}")
    plt.xlabel("state")
    plt.ylabel("fatalities per 10k residents") 
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def fat_state_year(df, states, years):    
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),
                                                 int(years[1])) )) ]
    group_df = new_df.groupby(['st', 'yr'])['fat'].sum().reset_index()
    sns.lineplot(data=group_df, x='yr', y='fat', hue='st', marker='o')
    plt.title(f"Fatalities for states in the years {years[0]} - {years[1]}")
    plt.xlabel("year")
    plt.ylabel("fatality")
    
def fat_state_year_10kppl(df, states, years):
    df['fat_per_ppl'] = df['fat'] / df['pop'] * 10000
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),
                                                 int(years[1])) )) ]
    group_df = new_df.groupby(['st', 'yr'])['fat_per_ppl'].sum().reset_index()
    sns.lineplot(data=group_df, x='yr', y='fat_per_ppl', hue='st', marker='o')
    plt.title(f"Fatalities for states in the years {years[0]} - {years[1]}")
    plt.xlabel("year")
    plt.ylabel("fatality")
    

''' FREQUENCIES '''
def frequency_years(df, states, years):
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),
                                                 int(years[1])) )) ]
    group_df = new_df.groupby(['st', 'yr'])['mo'].count().reset_index()
   
    sns.lineplot(data=group_df, x='yr', y='mo', hue='st', marker='o')
    plt.title(f"Frequency of tornados for states in the years {years[0]} - {years[1]}")
    plt.xlabel("year")
    plt.ylabel("number of confirmed tornados")
    
def frequency_years_10kppl(df, states, years):
    df['freq_per_ppl'] = 1 / df['pop'] * 10000
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),
                                                 int(years[1])) )) ]
    group_df = new_df.groupby(['st', 'yr'])['freq_per_ppl'].sum().reset_index()
    sns.lineplot(data=group_df, x='yr', y='freq_per_ppl', hue='st', marker='o')
    plt.title(f"Frequency of tornados for states in the years {years[0]} - {years[1]}")
    plt.xlabel("year")
    plt.ylabel("number of confirmed tornados")
    
''' TIME '''
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def time_of_day(df, states, years):
    df['hour'] = df['time'].str[:2]
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby(['hour', 'st'])['mo'].count()
    
    sns.lineplot(data = group_df.to_frame(), x = 'hour', y = 'mo', hue='st')
    plt.title(f"Frequency of tornados for states in the years {years[0]} - {years[1]}")
    plt.xlabel("hour of day (in CST)")
    plt.ylabel("total tornados") 
    
# df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
def time_of_year(df, states, years):
    new_df = df[df['st'].isin(states)]
    new_df = new_df[new_df['yr'].isin(list(range(int(years[0]),int(years[1]) ))) ]
    group_df = new_df.groupby(['mo', 'st'])['dy'].count()
    
    sns.lineplot(data = group_df.to_frame(), x = 'mo', y = 'dy', hue='st')
    plt.title(f"Frequency of tornados for states in the years {years[0]} - {years[1]}")
    plt.xlabel("month of year")
    plt.ylabel("total tornados per month") 