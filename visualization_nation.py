import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import st_folium

class nationVis:
    def __init__(self, df, start_year, end_year):
        self.df = df
        self.years = [start_year, end_year]

    ''' losses '''
    def infl_adj_loss(self):
        new_df = self.df[self.df['yr'].isin(range(self.years[0], self.years[1]))]
        new_df['loss_adjusted'] = new_df['damage'] * new_df['CPI_Multiplier'] 
        group_df = new_df.groupby(['yr'])['loss_adjusted'].sum().reset_index()

        fig, ax = plt.subplots()
        sns.lineplot(data=group_df, x='yr', y='loss_adjusted', marker='o', ax=ax)
        ax.set_title(f"Total inflation adjusted loss in the USA for the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("year")
        ax.set_ylabel("dollar loss, inflation adjusted for 8/24")

        return fig
    
    ''' fatalities '''
    
    def fat(self):
        new_df = self.df[self.df['yr'].isin(range(self.years[0], self.years[1]))]
        new_df = new_df.groupby(['yr'])['fat'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.lineplot(data=new_df, x='yr', y='fat', marker='o', ax=ax)
        ax.set_title(f"Fatalities in the USA for the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("year")
        ax.set_ylabel("fatalities") 

        return fig

    def fat_10kppl(self):
        new_df = self.df[self.df['yr'].isin(range(self.years[0], self.years[1]))]
        new_df = new_df.groupby(['yr', 'st']).agg({'pop': 'sum','fat': 'sum'}).reset_index()
        new_df2 = new_df.groupby(['yr']).agg({'pop': 'sum', 'fat': 'sum'}).reset_index()
        new_df2['fat_pop'] = new_df2['fat'] / new_df2['pop']
        
        fig, ax = plt.subplots()
        sns.lineplot(data=new_df2, x='yr', y='fat_pop', marker='o', ax=ax)
        ax.set_title(f"Fatalities in the USA for the years {self.years[0]} - {self.years[1]}, per 10k residents")
        ax.set_xlabel("year")
        ax.set_ylabel("fatalities per 10k residents") 

        return fig