import streamlit as st
import os
import pandas as pd

from dotenv import load_dotenv
from utils.b2 import B2
from streamlit_folium import st_folium
import visualizations as vis
from botocore.exceptions import ClientError

from visualizations import stateVis
from Nation_Visualisation import nationVis
from Seasons_Visualizations import plot_seasons
from Region_Visualisations import regionVis
from Division_Visualisation import DivisionVis
from Dimensions_Visualisations import DimensionsVis

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

# DEFAULT SHOULD BE FALSE
local_test = False

if local_test: 
    #''' RUN DATA LOCALLY '''
    df = pd.read_csv('Tornado_clean.csv')
else: 
    #''' RUN DATA REMOTE '''
    load_dotenv()
    REMOTE_DATA = 'Tornado_clean.csv' # name of the file
    KEY_ID = os.getenv('B2_KEYID')
    SECRET_KEY = os.getenv('B2_APPKEY')
    # load Backblaze connection
    b2 = B2(endpoint='https://s3.us-east-005.backblazeb2.com',
            key_id=KEY_ID,
            secret_key=SECRET_KEY)
    @st.cache_data
    def get_data():
        # collect data frame of reviews and their sentiment
        b2.set_bucket('tornado-second-version')
        df= b2.get_df(REMOTE_DATA)
        
        return df

    try:
        df = get_data()
    except ClientError as e:
        st.error("We're sorry, but our bandwidth cap has been reached for the day.  Please come again tomorrow!\
            If this problem persists, please contact one of us via our GitHub: https://github.com/Vigneshwarr3/Tornado_project")
        st.stop()


create_sidebar()


# side bar
with st.sidebar:
    selection = st.radio(
        "Choose a filter to explore",
        #("Nation", "Region", "Division", "State"),
        ("State", "Division", "Region", "Nation", "Dimensions", "Seasons"),
    )
    if selection != "Nation" and selection != "Seasons": 
        year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2013,2023))
    elif selection == "Seasons":
        pass
    else:
        year = st.selectbox("Select a year", df['yr'].sort_values(ascending=False).unique(), index = 1)

    if selection == "State":
        states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())
    elif selection == "Division":
        division = st.multiselect("Select Divisions: ", df.sort_values(by=['Division'], ascending=True)['Division'].unique())
        
    elif selection == "Dimensions":
        states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())

# creates drop down options for users to select their desired inputs
if(selection == "State"):
    
    st.write("# State")
    st.write("")
    # executes code if at least one state is selected
    if(len(states) in range(1,7)):
        # the class for this would be found in the visualizations py file
        # from visualizations import stateVis # <- new way to import
        input = stateVis(df, states, year_new[0], year_new[1])
        
        # all the visualizations
        # put the maps here, idk how to do those
        st.header("Damage Adjusted for Inflation")
        damage_col1, damage_col2 = st.columns(2)
        damage_col1.pyplot(input.infl_adj_loss_state())
        damage_col2.pyplot(input.infl_adj_loss_state_per10ksqmi())
        st.pyplot(input.infl_adj_loss_state_year())

        new_df = df[df['State'].isin(states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(year_new[0]),int(year_new[1]) ))) ]

        st.header("Fatalities")
        if new_df['fat'].sum() > 0:
            fatal_col1, fatal_col2 = st.columns(2)
            fatal_col1.pyplot(input.fat_state())
            fatal_col2.pyplot(input.fat_state_10ksqmi())
            fatal_col1.pyplot(input.fat_state_10kppl())
            st.pyplot(input.fat_state_year())
            st.pyplot(input.fat_state_year_10kppl())
        else:
            st.write(f"There were no fatalities in the selected states between the years {year_new[0]} and {year_new[1]}")

        st.header("Frequencies of Tornados")
        st.pyplot(input.frequency_years())
        st.pyplot(input.frequency_years_10kppl())
        st.pyplot(input.time_of_day())
        st.pyplot(input.time_of_year())
        st.pyplot(input.frequency_months())

    elif len(states) > 6:
        st.write("Please select less than 7 states to view visualisations!")
        #st.markdown("![Alt Text](https://lh4.googleusercontent.com/proxy/XR2ptXGHlegbGutJAvnZzI06FrdMdNYAbDpKJZs_rrvaUIHfZSdXcRneexVcnA)")
        
    else:
        input = stateVis(df, states, year_new[0], year_new[1])
        st.write("Select states from the side bar, not more than 6, to view visualizations!")
        #st.markdown("![Alt Text](https://media.tenor.com/4Cv1vFQWr24AAAAi/%D1%83%D1%82%D0%BA%D0%B0.gif)")
        st.write("To give you an idea of most affected states over a decade refer the below plot.")
        st.pyplot(input.top_10_tornadoes())

elif(selection == "Division"):

    st.write("# Division")
    st.write("")
    
    if(len(division) > 0):
        # st.write("This area of code is being worked on!  No visualizations available at this time.")
        # need to make a py file with divsion class and visualizations 
        div_input = DivisionVis(df, division, year_new[0], year_new[1])

        st.header("🔻 Loss")
        st.pyplot(div_input.infl_adj_loss_division())

        st.header("Fatalities")
        st.pyplot(div_input.fat_division())

    else:
        st.write("Select a division to see visualizations!")
elif(selection == "Seasons"):

    st.header("Seasons")
    st.write("### This visualization helps you to compare tornado activity across different seasons, revealing seasonal trends.")
    st.write("")
    st.pyplot(plot_seasons(df))

elif(selection == "Region"):

    st.write("# Region")
    st.write("")

    region_input = regionVis(df, year_new[0], year_new[1])

    col1, col2 = st.columns(2)
    with col1:
        st.header("🔻 Loss")
        st.pyplot(region_input.infl_adj_loss_region())
    with col2:
        st.header("Fatalities")
        st.pyplot(region_input.fat_region())

    st.pyplot(region_input.fat_region_year())
    st.pyplot(region_input.damage_region_year())
    st.pyplot(region_input.frequency_years())


elif(selection == "Nation"):
    st.write("# Nation")
    st.write("")
    nation_input = nationVis(df, year)
    
    # displaying the metrics
    st.write(f"#### Total metric for the year {year}")
    nation_input.show_metrics()

    # displaying the map 
    st.write("\n")
    st.write('''### Heat map 🔥''')
    st.write('''Below is a heat map. Darker the color the more tornado got affected. And black color means "No Data Found" for that year and state.''')
    st.write('''Hover over each state to view metrics for each state!''')
    st_folium(nation_input.folium_map(), width=750, height=450)

    # displaying the map 
    st.write('''### Tracing Tornado's path 🌀''')
    st.write('''We have tried to trace the tornado's path based on the start and end coordinates. Thickness of the line traced is relative to the size of the actual tornado itself, so that you can have a sense of how big of a tornado affected in a particular area.''')
    st.write('''Hover over each path to view the metrics!''')
    st_folium(nation_input.tornado_paths(), width=750, height=450)

elif(selection == "Dimensions"):
    st.write("# Dimensions Diagnosis")
    
    Dim_input = DimensionsVis(df, states, year_new[0], year_new[1])
    
    if len(states) == 1:
        st.pyplot(Dim_input.tornado_width_over_time())
        st.pyplot(Dim_input.tornado_length_over_time())

        st.pyplot(Dim_input.magnitude_vs_fatalities())
        st.pyplot(Dim_input.visualize_high_intensity_tornadoes())
    else:
        st.write("Please select one state for visualisations!")
    
    


