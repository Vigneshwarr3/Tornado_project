import streamlit as st
import folium

class nationVis:
    def __init__(self, df, year):
        self.df = df
        self.year = year
        self.fatal_loss = df\
                            [['yr','State', 'om', 'fat', 'closs', 'loss', 'inj']]\
                            .groupby(['yr', 'State'])\
                            .aggregate({"fat":"sum", "om":'nunique', 'closs': 'sum', 'loss': 'sum', 'inj': 'sum', }).reset_index()
        self.df_year = self.fatal_loss[self.fatal_loss['yr'] == year]

    def show_metrics(self):

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Fatalities", sum(self.df_year['fat']))
        with col2:
            st.metric("Number of Tornadoes affected", self.df_year['om'].nunique())
        with col3:
            st.metric("Total Injuries", sum(self.df_year['inj']))

        col4, col5 = st.columns(2)
        with col4:
            st.metric("Total Crop loss",'${:,}'.format(sum(self.df_year['closs'])))
        with col5:
            st.metric("Total Property loss",'${:,}'.format(sum(self.df_year['loss'])))

    # Instead of having the folium maps in the app.py file, I'm (vigneshwar) moving the here into a function, so that its neat.
    

    ### Folium map ###
    def folium_map(self):
        geojson_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

        m = folium.Map(location=[42, -98], zoom_start=4)

        folium.Choropleth(
            geo_data=geojson_url,
            name='choropleth',
            data=self.df_year,
            columns=['State', 'om'], 
            key_on='feature.properties.name',
            fill_color='Oranges',
            line_opacity=0.5,
            legend_name=f'Number of Tornadoes in the year {self.year}'
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
        for feature in tooltip_layer.data['features']:
            state_name = feature['properties']['name']
            tooltip_content = get_tooltip_content(state_name, self.df_year)
            feature['properties']['tooltip'] = tooltip_content  # Add tooltip content for each state

        tooltip_layer.add_child(folium.features.GeoJsonTooltip(fields=['tooltip'], labels=False))

        tooltip_layer.add_to(m)

        return m

    ####### Tornado paths #########
    def tornado_paths(self):

        tornado_location = self.df[['om', 'yr', 'slat','slon', 'elat', 'elon', 'len', 'wid']]
        tornado_location = tornado_location[~ tornado_location.duplicated()]

        tornado_paths = tornado_location[tornado_location['yr'] == self.year]

        tornado_map = folium.Map(location=[42, -98], zoom_start=4)

        for _, row in tornado_paths.iterrows():
            weight_ = ((row['wid'] - min(tornado_paths['wid'])) / (max(tornado_paths['wid']) - min(tornado_paths['wid'])))*10
            start = [row['slat'], row['slon']]
            end = [row['elat'], row['elon']]
            weight = row['wid']
            hover_message = f"<b> Tornado Dimensions</b>  <br> Length: {row['len']} miles <br>Width: {row['wid']} yards"
            
            folium.PolyLine(locations=[start, end], color="red", weight=weight_, tooltip=hover_message).add_to(tornado_map)
        
        return tornado_map