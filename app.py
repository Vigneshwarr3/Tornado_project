import os

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from utils.b2 import B2
from streamlit_folium import st_folium
import visualizations as vis
from tornado4 import analyze_tornado_dataset,plot_top_tornado_states,plot_tornadoes_by_month_for_year,plot_tornadoes_by_state_and_year,plot_yearly_trend,plot_monthly_trend
from botocore.exceptions import ClientError

# ------------------------------------------------------
#                      APP CONSTANTS
# ------------------------------------------------------
REMOTE_DATA = 'Tornado_clean.csv' # name of the file


# ------------------------------------------------------
#                        CONFIG
# ------------------------------------------------------
load_dotenv()

# load Backblaze connection
b2 = B2(endpoint='https://s3.us-east-005.backblazeb2.com',
        key_id='005ad5797e6974d0000000002',
        secret_key='K005q7mZ1SwcxHEotsKEd7mnihbmkVg')

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket('tornado-second-version')
    df= b2.get_df(REMOTE_DATA)

    fatal_loss = df\
    [['yr','State', 'om', 'fat', 'closs', 'loss', 'inj']]\
    .groupby(['yr', 'State'])\
    .aggregate({"fat":"sum", "om":'nunique', 'closs': 'sum', 'loss': 'sum', 'inj': 'sum', }).reset_index()
    
    return df, fatal_loss

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 0 : Overview
# ------------------------------
st.write('''# Project Tornado''')

df, fatal_loss = get_data()

# ------------------------------
# PART 1 : Filter Data
# ------------------------------



s_df = pd.read_csv("https://raw.githubusercontent.com/Vigneshwarr3/Tornado_project/refs/heads/saipranam/data/1950-2023_all_tornadoes.csv")



#------ Sai Pranam---------
#analyze_tornado_dataset(s_df)
st.subheader("Top 10 States with Highest Tornados per Square Mile")
plot_top_tornado_states(s_df)
# User inputs
state = st.text_input("Enter the state abbreviation (e.g., TX, FL):", "").upper()
years_input = st.text_input("Enter one or two years (comma-separated, e.g., '2000' or '2000, 2020'):")

if state and years_input:
    years = list(map(int, years_input.split(',')))

    # Determine which function to call
    if len(years) == 1:
        st.subheader(f"Tornado Analysis for {state} in {years[0]}")
        plot_tornadoes_by_month_for_year(s_df, years[0], state)
    else:
        st.subheader(f"Tornado Analysis for {state} from {years[0]} to {years[-1]}")
        plot_tornadoes_by_state_and_year(s_df, state, years)
# Sidebar for trend analysis
st.sidebar.title("Analysis Options")
trend_option = st.sidebar.radio("Select Analysis Type:", 
                                    ['Yearly Trend', 'Monthly Trend'])

# Yearly trend
if trend_option == 'Yearly Trend':
    st.subheader("Yearly Trend of Tornado Occurrences")
    plot_yearly_trend(s_df)

# Monthly trend
elif trend_option == 'Monthly Trend':
    st.subheader("Monthly Trend of Tornado Occurrences")
    plot_monthly_trend(s_df)

# State and year-specific analysis
elif trend_option == 'State/Year Analysis':
    state = st.text_input("Enter the state abbreviation (e.g., TX, FL):", "").upper()
    years_input = st.text_input("Enter one or two years (comma-separated, e.g., '2000' or '2000, 2020'):")

    if state and years_input:
        years = list(map(int, years_input.split(',')))

        # Determine which function to call
        if len(years) == 1:
            st.subheader(f"Tornado Analysis for {state} in {years[0]}")
            plot_tornadoes_by_month_for_year(s_df, years[0], state)
        else:
            st.subheader(f"Tornado Analysis for {state} from {years[0]} to {years[-1]}")
            plot_tornadoes_by_state_and_year(s_df, state, years) 

#-----------------



# need to update this from 'Year' to 'yr' once we update our initial df
year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2020, 2023))
year = year_new[0]
year_end = year_new[0]

# we can make more like regions, but we might want to reformat this
states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())

df_year = fatal_loss[fatal_loss['yr'] == year]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Fatalities", sum(df_year['fat']))
with col2:
    st.metric("Number of Tornadoes affected", df_year['om'].nunique())
with col3:
    st.metric("Total Injuries", sum(df_year['inj']))

col4, col5 = st.columns(2)
with col4:
    st.metric("Total Crop loss",'${:,}'.format(sum(df_year['closs'])))
with col5:
    st.metric("Total Property loss",'${:,}'.format(sum(df_year['loss'])))

# displaying the map 
st_folium(vis.folium_map(df_year, year), width=700, height=450)

# displaying the map 
st_folium(vis.tornado_paths(df, year), width=700, height=450)

# we can make more like regions, but we might want to reformat this
states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())

# a new test plot from visualisations.py
st.pyplot(vis.infl_adj_loss_state(df, states, [year, year_end]))