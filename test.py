import os
import streamlit as st
import pandas as pd
from visualizations import stateVis

from Nation_Visualisation import nationVis
from Region_Visualisations import regionVis
from Division_Visualisation import DivisionVis

#from visualization_nation import nationVis

import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

df = pd.read_csv('Tornado_clean.csv')

### This is just a test to see how the class would work
### a better version should be available from imported vis file
class test:
    def __init__(self, df, states, start_year, end_year):
        self.df = df
        self.states = states
        self.years = [start_year, end_year]

# side bar
with st.sidebar:
    selection = st.radio(
        "Choose a filter to explore",
        ("Nation", "Region", "Division", "State")
    )

st.write("# Tornado Project")

# creates drop down options for users to select their desired inputs
if(selection == "State"):
    year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2013,2023))
    states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())
    
    # executes code if at least one state is selected
    if(len(states) > 0):
        # the class for this would be found in the visualizations py file
        # from visualizations import stateVis # <- new way to import
        input = stateVis(df, states, year_new[0], year_new[1])
        
        # all the visualizations
        # put the maps here, idk how to do those
        st.header("Damage Adjusted for Inflation")
        st.pyplot(input.infl_adj_loss_state())
        st.pyplot(input.infl_adj_loss_state_year())
        st.pyplot(input.infl_adj_loss_state_per10ksqmi())

        st.header("Fatalities")
        st.pyplot(input.fat_state())
        st.pyplot(input.fat_state_10ksqmi())
        st.pyplot(input.fat_state_10kppl())
        st.pyplot(input.fat_state_year())
        st.pyplot(input.fat_state_year_10kppl())

        st.header("Frequencies of Tornados")
        st.pyplot(input.frequency_years())
        st.pyplot(input.frequency_years_10kppl())
        st.pyplot(input.time_of_day())
        st.pyplot(input.time_of_year())

    else:
        st.write("Select states to see visualizations!")

elif(selection == "Division"):
    year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2013,2023))
    division = st.multiselect("Select Divisions: ", df.sort_values(by=['Division'], ascending=True)['Division'].unique())
    if(len(division) > 0):
        # st.write("This area of code is being worked on!  No visualizations available at this time.")
        # need to make a py file with divsion class and visualizations 
        div_input = DivisionVis(df, division, year_new[0], year_new[1])

        st.pyplot(div_input.infl_adj_loss_division())
        st.pyplot(div_input.fat_division())

    else:
        st.write("Select divisions to see visualizations!")

elif(selection == "Region"):
    year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2013,2023)) 

    region_input = regionVis(df, year_new[0], year_new[1])

    col1, col2 = st.columns(2)
    with col1:
        st.header("Damage")
        st.pyplot(region_input.infl_adj_loss_region())
    with col2:
        st.header("Fatalities")
        st.pyplot(region_input.fat_region())

    year = st.selectbox("Select a year", df['yr'].unique(), index = 73)
    nation_input = nationVis(df, year)
    
    # displaying the metrics
    nation_input.show_metrics()

    # displaying the map 
    st.write("\n")
    st.write('''### Hover over each state to see the metrics!''')
    st_folium(nation_input.folium_map(), width=700, height=450)

    # displaying the map 
    st_folium(nation_input.tornado_paths(), width=700, height=450)
    
    # do we want to add multiple years?
'''
    # this is the nation option, no inputs needed, USA is the only nation in question
    input = nationVis(df, year_new[0], year_new[1])

    st.header("Damage Adjusted for Inflation")
    st.pyplot(input.infl_adj_loss())

    st.header("Fatalities")
    st.pyplot(input.fat())
    st.pyplot(input.fat_10kppl())
'''



