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

'''
11/14 NEW UPDATE FOR FORMAT
To meet requirements, and honestly it's kind of nice, everything here will be a class
Not all the functions are currently saved to be like that... so this will need some updating
mostly just slapping a "self" in front of a lot of things.  Should be pretty chill.
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import st_folium

class stateVis:
    def __init__(self, df, states, start_year, end_year):
        self.df = df
        self.states = states
        self.years = [start_year, end_year]

    ''' INFLATION ADJUSTED LOSSES '''

    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def infl_adj_loss_state(self):
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['loss_adjusted'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'loss_adjusted', ax=ax)
        ax.set_title(f"Total inflation adjusted loss for states in the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("state")
        ax.set_ylabel("dollar loss, inflation adjusted for 8/24")      

        return fig        
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def infl_adj_loss_state_year(self):    
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1])) )) ]
        group_df = new_df.groupby(['State', 'yr'])['loss_adjusted'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='loss_adjusted', hue='State', marker='o', ax=ax)
        ax.set_title(f"Inflation adjusted loss for states in the years {self.years[0]} - {self.years[1]}, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("dollar loss, inflation adjusted for 8/24")

        return fig
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end] 
    def infl_adj_loss_state_per10ksqmi(self):
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        self.df['loss_per_area'] = self.df['loss_adjusted'] / self.df['Total area'] * 10000
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['loss_per_area'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'loss_per_area', ax=ax)
        ax.set_title(f"Total inflation adjusted loss for states in the years {self.years[0]} - {self.years[1]}, per 10k square miles")
        ax.set_xlabel("state")
        ax.set_ylabel("dollar loss per 10k sq mi, inflation adjusted for 8/24") 

        return fig
        
        
    ''' FATALITIES '''

    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def fat_state(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['fat'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'fat', ax=ax)
        ax.set_title(f"Total fatalities for states in the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("state")
        ax.set_ylabel("fatalities") 

        return fig
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def fat_state_10ksqmi(self):
        self.df['fat_per_area'] = self.df['fat'] / self.df['Total area'] * 10000
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['fat_per_area'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'fat_per_area', ax=ax)
        ax.set_title(f"Fatalities for states in the years {self.years[0]} - {self.years[1]}, per 10k square miles")
        ax.set_xlabel("state")
        ax.set_ylabel("fatalities per 10k sq mi") 

        return fig
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def fat_state_10kppl(self):
        self.df['fat_per_ppl'] = self.df['fat'] / self.df['pop'] * 10000
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['fat_per_ppl'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'fat_per_ppl', ax=ax)
        ax.set_title(f"Fatalities for states in the years {self.years[0]} - {self.years[1]}, per 10k residents")
        ax.set_xlabel("state")
        ax.set_ylabel("fatalities per 10k residents") 

        return fig
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def fat_state_year(self):    
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]), int(self.years[1])) )) ]
        group_df = new_df.groupby(['State', 'yr'])['fat'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='fat', hue='State', marker='o', ax=ax)
        ax.set_title(f"Fatalities for states in the years {self.years[0]} - {self.years[1]}, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("fatality")

        return fig
        
    def fat_state_year_10kppl(self):
        self.df['fat_per_ppl'] = self.df['fat'] / self.df['pop'] * 10000
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]), int(self.years[1])) )) ]
        group_df = new_df.groupby(['State', 'yr'])['fat_per_ppl'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='fat_per_ppl', hue='State', marker='o', ax=ax)
        ax.set_title(f"Fatalities for states in the years {self.years[0]} - {self.years[1]}, per 10k residents")
        ax.set_xlabel("year")
        ax.set_ylabel("fatalities per 10k residents")

        return fig
        

    ''' FREQUENCIES '''
    def frequency_years(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]), int(self.years[1])) )) ]
        group_df = new_df.groupby(['State', 'yr'])['mo'].count().reset_index()
    
        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='mo', hue='State', marker='o', ax=ax)
        ax.set_title(f"Frequency of tornados for states in the years {self.years[0]} - {self.years[1]}, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("number of confirmed tornados")

        return fig
        
    def frequency_years_10kppl(self):
        self.df['freq_per_ppl'] = 1 / self.df['pop'] * 10000
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]), int(self.years[1])) )) ]
        group_df = new_df.groupby(['State', 'yr'])['freq_per_ppl'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='freq_per_ppl', hue='State', marker='o', ax=ax)
        ax.set_title(f"Frequency of tornados for states in the years {self.years[0]} - {self.years[1]}, per 10k residents")
        ax.set_xlabel("year")
        ax.set_ylabel("number of confirmed tornados, per 10k residents")

        return fig
        
    ''' TIME '''
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def time_of_day(self):
        self.df['hour'] = self.df['time'].str[:2]
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby(['hour', 'State'])['mo'].count()
        
        fig, ax = plt.subplots()
        sns.lineplot(data = group_df.to_frame(), x = 'hour', y = 'mo', hue='State', ax=ax)
        ax.set_title(f"Frequency of tornados for states in the years {self.years[0]} - {self.years[1]} in each hour of the day (CST)")
        ax.set_xlabel("hour of day (in CST)")
        ax.set_ylabel("total tornados") 

        return fig
        
    # df is cleaned tornado, states is array ['x','y','z'], years is [start,end]
    def time_of_year(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby(['mo', 'State'])['dy'].count()
        
        fig, ax = plt.subplots()
        sns.lineplot(data = group_df.to_frame(), x = 'mo', y = 'dy', hue='State', ax=ax)
        ax.set_title(f"Frequency of tornados for states in the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("month of year")
        ax.set_ylabel("total tornados per month") 

        return fig

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