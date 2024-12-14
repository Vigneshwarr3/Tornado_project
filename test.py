import os
import streamlit as st
import pandas as pd
from visualizations import stateVis

#from visualization_nation import nationVis

import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

df = pd.read_csv('Tornado_clean.csv')

states = ['Texas', 'Oklahoma']
year_new = [2000, 2020]

input = stateVis(df, states, year_new[0], year_new[1])

if input:
    st.write("class exists")

try:
    st.pyplot(input.infl_adj_loss_state())
    st.pyplot(input.infl_adj_loss_state_year())
    st.pyplot(input.infl_adj_loss_state_per10ksqmi())
    st.write("This works")
except Exception as e:
    st.write("Plot setup failed")

# tests complete, class and print functions work as expected
# can run this locally to confirm

st.stop()