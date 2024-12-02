import os
import streamlit as st
import pandas as pd
#import visualizations as vis
from visualizations import stateVis
from visualization_nation import nationVis
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('Tornado_clean.csv')

### This is just a test to see how the class would work
### a better version should be available from imported vis file
class test:
    def __init__(self, df, states, start_year, end_year):
        self.df = df
        self.states = states
        self.years = [start_year, end_year]
    
    def infl_adj_loss_state(self):
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('State')['loss_adjusted'].sum().reset_index()
        
        sns.barplot(data = group_df.iloc[0:10], x = 'State', y = 'loss_adjusted')
        plt.title(f"Inflation adjusted loss for states in the years {self.years[0]} - {self.years[1]}")
        plt.xlabel("state")
        plt.ylabel("dollar loss, inflation adjusted for 8/24") 

        return plt


# side bar
with st.sidebar:
    selection = st.radio(
        "Choose a filter to explore",
        ("Nation", "Region", "Division", "State")
    )

# creates titles and short description on how the webpage works
st.title("USA Tornado Visualizations")
st.write("Select filters such as the start year, end year, and any subset of the USA you'd like to see insights for!")
st.write("Please note that collection of data has changed over time, and some assumptions have been made to make this data readily \
        available for your viewing.  Please view our 'Extra Information' page to learn more about these assumptions and limitations \
        of this data.")

year_new = st.slider("Select the year range", min(df['yr']), max(df['yr']), (2013,2023))
# idea to add in warning about assumptions
if(year_new[0] < 1996):
    st.write("Damage estimates are signficantly less accurate before 1996.  Please view our 'Extra Information' page for more information.")


# creates drop down options for users to select their desired inputs
if(selection == "State"):
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
    division = st.multiselect("Select Divisions: ", df.sort_values(by=['Division'], ascending=True)['Division'].unique())
    if(len(division) > 0):
        st.write("This area of code is being worked on!  No visualizations available at this time.")
        # need to make a py file with divsion class and visualizations 
    else:
        st.write("Select divisions to see visualizations!")

elif(selection == "Region"):
    region = st.multiselect("Select Regions: ", df.sort_values(by=['Region'], ascending=True)['Region'].unique())  
    if(len(region) > 0):
        st.write("This area of code is being worked on!  No visualizations available at this time.") 
        # need to make a py file with region class and visualizations 
    else:
        st.write("Select regions to see visualizations!")

else:
    # this is the nation option, no inputs needed, USA is the only nation in question
    input = nationVis(df, year_new[0], year_new[1])

    st.header("Damage Adjusted for Inflation")
    st.pyplot(input.infl_adj_loss())

    st.header("Fatalities")
    st.pyplot(input.fat())
    st.pyplot(input.fat_10kppl())






