import os
import streamlit as st
from dotenv import load_dotenv

from utils.b2 import B2
import folium
from streamlit_folium import st_folium

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
    [['Year','State_new', 'Tornado_number', 'Fatalities', 'Crop_loss', 'Property_loss', 'Injuries']]\
    .groupby(['Year', 'State_new'])\
    .aggregate({"Fatalities":"sum", "Tornado_number":'nunique', 'Crop_loss': 'sum', 'Property_loss': 'sum', 'Injuries': 'sum', }).reset_index()
    
    return df, fatal_loss

# ------------------------------------------------------
#                         APP
# ------------------------------------------------------
# ------------------------------
# PART 0 : Overview
# ------------------------------
st.write(
'''
# Project Tornado
''')

#df = pd.read_csv('Tornado_clean.csv')
df, fatal_loss = get_data()
# fatal_loss = df\
#     [['Year','State_new', 'Tornado_number', 'Fatalities', 'Crop_loss', 'Property_loss', 'Injuries']]\
#     .groupby(['Year', 'State_new'])\
#     .aggregate({"Fatalities":"sum", "Tornado_number":'nunique', 'Crop_loss': 'sum', 'Property_loss': 'sum', 'Injuries': 'sum', }).reset_index()

# ------------------------------
# PART 1 : Filter Data
# ------------------------------
year = st.selectbox("Select a year:",
                     df['Year'].unique())

df_year = df_year = fatal_loss[fatal_loss['Year'] == year]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Fatalities", sum(df_year['Fatalities']))
with col2:
    st.metric("Number of Tornadoes affected", df_year['Tornado_number'].nunique())
with col3:
    st.metric("Total Injuries", sum(df_year['Injuries']))

col4, col5 = st.columns(2)
with col4:
    st.metric("Total Crop loss",'${:,}'.format(sum(df_year['Crop_loss'])))
with col5:
    st.metric("Total Property loss",'${:,}'.format(sum(df_year['Property_loss'])))

### Folium map ###

geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

m = folium.Map(location=[42, -98], zoom_start=4)

folium.Choropleth(
    geo_data=geojson_url,
    name='choropleth',
    data=df_year,
    columns=['State_new', 'Tornado_number'], 
    key_on='feature.properties.name',
    fill_color='Oranges',
    line_opacity=0.5,
    legend_name=f'Number of Tornadoes in the year {year}'
).add_to(m)

def get_tooltip_content(state_name):
    row = df_year[df_year['State_new'] == state_name]
    if state_name in df_year['State_new'].values:
        content = f"""
        <b>State:</b> {state_name}<br>
        <b>Tornadoes:</b> {row['Tornado_number'].values[0]}<br>
        <b>Fatalities:</b> {row['Fatalities'].values[0]}<br>
        <b>Crop Loss:</b> ${row['Crop_loss'].values[0]:,.0f}<br>
        <b>Property Loss:</b> ${row['Property_loss'].values[0]:,.0f}<br>
        <b>Injuries:</b> {row['Injuries'].values[0]}
        """
    else:
        content = f"<b>State:</b> {state_name}<br>No data available"
    
    return content

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
    tooltip_content = get_tooltip_content(state_name)
    feature['properties']['tooltip'] = tooltip_content  # Add tooltip content for each state

tooltip_layer.add_child(folium.features.GeoJsonTooltip(fields=['tooltip'], labels=False))

tooltip_layer.add_to(m)

# displaying the map 
st_folium(m, width=700, height=450)


####### Tornado paths #########

tornado_location = df[['Tornado_number', 'Year', 'Start_lat','Start_lon', 'End_lat', 'End_lon', 'Length', 'Width']]
tornado_location = tornado_location[~ tornado_location.duplicated()]

tornado_paths = tornado_location[tornado_location['Year'] == year]

tornado_map = folium.Map(location=[42, -98], zoom_start=4)

for _, row in tornado_paths.iterrows():
    weight_ = ((row['Width'] - min(tornado_paths['Width'])) / (max(tornado_paths['Width']) - min(tornado_paths['Width'])))*10
    start = [row['Start_lat'], row['Start_lon']]
    end = [row['End_lat'], row['End_lon']]
    weight = row['Width']
    hover_message = f"<b> Tornado Dimensions</b>  <br> Length: {row['Length']} miles <br>Width: {row['Width']} yards"
    
    folium.PolyLine(locations=[start, end], color="red", weight=weight_, tooltip=hover_message).add_to(tornado_map)

# displaying the map 
st_folium(tornado_map, width=700, height=450)