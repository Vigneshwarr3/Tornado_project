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
import folium
from streamlit_folium import st_folium

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

    return plt         
    
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

# Instead of having the folium maps in the app.py file, I'm (vigneshwar) moving the here into a function, so that its neat.

def get_tooltip_content(state_name, df_year):
    row = df_year[df_year['State'] == state_name]
    if state_name in df_year['State'].values:
        content = f"""
        <b>State:</b> {state_name}<br>
        <b>Tornadoes:</b> {row['om'].values[0]}<br>
        <b>Fatalities:</b> {row['fat'].values[0]}<br>
        <b>Crop Loss:</b> ${row['closs'].values[0]:,.0f}<br>
        <b>Property Loss:</b> ${row['loss'].values[0]:,.0f}<br>
        <b>Injuries:</b> {row['inj'].values[0]}
        """
    else:
        content = f"<b>State:</b> {state_name}<br>No data available"
    
    return content

### Folium map ###
def folium_map(df_year, year):
    geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

    m = folium.Map(location=[42, -98], zoom_start=4)

    folium.Choropleth(
        geo_data=geojson_url,
        name='choropleth',
        data=df_year,
        columns=['State', 'om'], 
        key_on='feature.properties.name',
        fill_color='Oranges',
        line_opacity=0.5,
        legend_name=f'Number of Tornadoes in the year {year}'
    ).add_to(m)

    tooltip_layer = folium.GeoJson(
        geojson_url,
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'black', 'weight': 1, 'fillOpacity': 0},
        tooltip=folium.GeoJsonTooltip(
            fields=['name'],  # Field from GeoJSON to use for tooltips
            aliases=['State:'],  # Label for the field
            localize=True,
            sticky=False,
            labels=True
        ),
        highlight_function=lambda x: {'weight': 2, 'color': 'blue', 'fillOpacity': 0.7}
    )

    for feature in tooltip_layer.data['features']:
        state_name = feature['properties']['name']
        tooltip_content = get_tooltip_content(state_name, df_year)
        feature['properties']['tooltip'] = tooltip_content  # Add tooltip content for each state

    tooltip_layer.add_child(folium.features.GeoJsonTooltip(fields=['tooltip'], labels=False))

    tooltip_layer.add_to(m)

    return m

####### Tornado paths #########
def tornado_paths(df, year):

    tornado_location = df[['om', 'yr', 'slat','slon', 'elat', 'elon', 'len', 'wid']]
    tornado_location = tornado_location[~ tornado_location.duplicated()]

    tornado_paths = tornado_location[tornado_location['yr'] == year]

    tornado_map = folium.Map(location=[42, -98], zoom_start=4)

    for _, row in tornado_paths.iterrows():
        weight_ = ((row['wid'] - min(tornado_paths['wid'])) / (max(tornado_paths['wid']) - min(tornado_paths['wid'])))*10
        start = [row['slat'], row['slon']]
        end = [row['elat'], row['elon']]
        weight = row['wid']
        hover_message = f"<b> Tornado Dimensions</b>  <br> Length: {row['len']} miles <br>Width: {row['wid']} yards"
        
        folium.PolyLine(locations=[start, end], color="red", weight=weight_, tooltip=hover_message).add_to(tornado_map)
    
    return tornado_map