import streamlit as st
import os
import pandas as pd
from visualizations import stateVis

from Nation_Visualisation import nationVis
from Region_Visualisations import regionVis
from Division_Visualisation import DivisionVis

import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Tornado trends", 
    page_icon="🌪️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

def create_sidebar():
    """Create a custom sidebar with enhanced styling"""
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h1>📈 Explore Tornado Trends</h1>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar description
    st.sidebar.markdown("""
    <p style="color: #B0BEC5; text-align: Left; padding: 0 15px;">
    Explore and analyze US Tornado trend based on different States, Regions and Divisions.
    </p>
    """, unsafe_allow_html=True)

df = pd.read_csv('Tornado_clean.csv')

create_sidebar()

# side bar
with st.sidebar:
    selection = st.radio(
        "Choose a filter to explore",
        ("Nation", "Region", "Division", "State")
    )
    if selection != "Nation": 
        year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2013,2023))
    else:
        year = st.selectbox("Select a year", df['yr'].sort_values(ascending=False).unique(), index = 0)

    if selection == "State":
        states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())
    elif selection == "Division":
        division = st.multiselect("Select Divisions: ", df.sort_values(by=['Division'], ascending=True)['Division'].unique())

# creates drop down options for users to select their desired inputs
if(selection == "State"):
    
    st.write("# State")
    st.write("")
    # executes code if at least one state is selected
    if(len(states) in range(2,7)):
        # the class for this would be found in the visualizations py file
        # from visualizations import stateVis # <- new way to import
        input = stateVis(df, states, year_new[0], year_new[1])
        
        # all the visualizations
        # put the maps here, idk how to do those
        st.header("Damage Adjusted for Inflation")
        damage_col1, damage_col2 = st.columns(2)
        damage_col1.pyplot(input.infl_adj_loss_state())
        damage_col2.pyplot(input.infl_adj_loss_state_per10ksqmi())
        damage_col1.pyplot(input.infl_adj_loss_state_year())

        st.header("Fatalities")
        fatal_col1, fatal_col2 = st.columns(2)
        fatal_col1.pyplot(input.fat_state())
        fatal_col2.pyplot(input.fat_state_10ksqmi())
        fatal_col1.pyplot(input.fat_state_10kppl())
        fatal_col2.pyplot(input.fat_state_year())
        fatal_col1.pyplot(input.fat_state_year_10kppl())

        st.header("Frequencies of Tornados")
        feq_col1, feq_col2 = st.columns(2)
        feq_col1.pyplot(input.frequency_years())
        feq_col2.pyplot(input.frequency_years_10kppl())
        feq_col1.pyplot(input.time_of_day())
        feq_col2.pyplot(input.time_of_year())

    elif len(states) > 6:
        st.write("Please select less than 7 states to view visualisations!")
        #st.markdown("![Alt Text](https://lh4.googleusercontent.com/proxy/XR2ptXGHlegbGutJAvnZzI06FrdMdNYAbDpKJZs_rrvaUIHfZSdXcRneexVcnA)")

    else:
        st.write("Select states, atleast 2 and not more than 6 states, to view visualizations!")
        

elif(selection == "Division"):

    st.write("# Division")
    st.write("")
    
    if(len(division) > 1):
        # st.write("This area of code is being worked on!  No visualizations available at this time.")
        # need to make a py file with divsion class and visualizations 
        div_input = DivisionVis(df, division, year_new[0], year_new[1])

        st.pyplot(div_input.infl_adj_loss_division())
        st.pyplot(div_input.fat_division())

    else:
        st.write("Select atleast 2 divisions to see visualizations!")

elif(selection == "Region"):

    st.write("# Region")
    st.write("")

    region_input = regionVis(df, year_new[0], year_new[1])

    col1, col2 = st.columns(2)
    with col1:
        st.header("Damage")
        st.pyplot(region_input.infl_adj_loss_region())
    with col2:
        st.header("Fatalities")
        st.pyplot(region_input.fat_region())

else:
    st.write("# Nation")
    st.write("")
    nation_input = nationVis(df, year)
    
    # displaying the metrics
    nation_input.show_metrics()

    # displaying the map 
    st.write("\n")
    st.write('''### Hover over each state to see the metrics!''')
    st_folium(nation_input.folium_map(), width=750, height=450)

    # displaying the map 
    st_folium(nation_input.tornado_paths(), width=750, height=450)
