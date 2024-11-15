import os
import streamlit as st
from dotenv import load_dotenv
from utils.b2 import B2
import folium
from streamlit_folium import st_folium
import visualizations as vis
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
b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_KEYID'],
        secret_key=os.environ['B2_APPKEY'])

# ------------------------------------------------------
#                        CACHING
# ------------------------------------------------------
@st.cache_data
def get_data():
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
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

try:
    df, fatal_loss = get_data()
except ClientError as e:
    st.error("We're sorry, but our bandwidth cap has been reached for the day.  Please come again tomorrow!\
        If this problem persists, please contact one of us via our GitHub: https://github.com/Vigneshwarr3/Tornado_project")
    st.stop()
    # If we want to create an alternative, like be sent to another page of our website, we can do that fs
    # but we don't have those capabilities rn, so I'm adding the stop function

# ------------------------------
# PART 1 : Filter Data
# ------------------------------

# need to update this from 'Year' to 'yr' once we update our initial df
year_new = st.slider("Select the year range", max(df['yr']), min(df['yr']), (2020, 2023))
year = year_new[0]
year_end = year_new[0]

# we can make more like regions, but we might want to reformat this
states = st.multiselect("Select States: ", df.sort_values(by=['State'], ascending=True)['State'].unique())

df_year = df_year = fatal_loss[fatal_loss['yr'] == year]

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

# a new test plot from visualisations.py
st.pyplot(vis.infl_adj_loss_state(df, states, [year, year_end]))