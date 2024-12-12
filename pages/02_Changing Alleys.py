import streamlit as st
import os
import pandas as pd

from dotenv import load_dotenv
from utils.b2 import B2
from streamlit_folium import st_folium
import visualizations as vis
from botocore.exceptions import ClientError

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
local_test = True
if local_test: 
    ''' RUN DATA LOCALLY '''
    df = pd.read_csv('Tornado_clean.csv')
else: 
    ''' RUN DATA REMOTE '''
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

# create visualizations locally here since this is last minute and I only want to make one file
TorAlley = ['Texas', 'Oklahoma', 'Kansas', 'Nebraska']
DixieAlley = ['Louisiana', 'Arkansas', 'Mississippi', 'Alabama', 'Georgia', 'Tennessee']
ALLEY = ['Tornado Alley', 'Dixie Alley']

df['Alley'] = df['State'].apply(lambda x: "Tornado Alley" if x in TorAlley else ("Dixie Alley" if x in DixieAlley else None) )

class Alley:
    def __init__(self, df):
        self.df = df

    def alley_freq(self):
        new_df = self.df[self.df['Alley'].isin(ALLEY)]
        new_df = new_df[new_df['yr'].isin(list(range(1970, 2023))) ]
        group_df = new_df.groupby(['Alley', 'yr'])['mo'].count().reset_index()
    
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=group_df, x='yr', y='mo', hue='Alley', ax=ax)
        ax.set_title(f"Frequency of tornados in the years 1970-2023, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("number of confirmed tornados")

        return fig
    
    def alley_deaths(self):
        new_df = self.df[self.df['Alley'].isin(ALLEY)]
        new_df = new_df[new_df['yr'].isin(list(range(1970, 2023))) ]
        group_df = new_df.groupby(['Alley', 'yr'])['fat'].sum().reset_index()
    
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=group_df, x='yr', y='fat', hue='Alley', ax=ax)
        ax.set_title(f"Deaths from tornados in the years 1970-2023, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("number of fatalities")

        return fig
    
    def alley_injuries(self):
        new_df = self.df[self.df['Alley'].isin(ALLEY)]
        new_df = new_df[new_df['yr'].isin(list(range(1970, 2023))) ]
        group_df = new_df.groupby(['Alley', 'yr'])['inj'].sum().reset_index()
    
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=group_df, x='yr', y='inj', hue='Alley', ax=ax)
        ax.set_title(f"Injuries from tornados in the years 1970-2023, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("number of injuries")

        return fig
    
    def death_per_tornado(self):
        new_df = self.df[self.df['Alley'].isin(ALLEY)]
        new_df = new_df[new_df['yr'].isin(list(range(1970, 2023))) ]
        group_df = new_df.groupby(['Alley', 'yr']).agg({
            'fat': 'sum',
            'mo': 'count'
        })
        group_df['DpT'] = group_df['fat'] / group_df['mo']
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=group_df, x='yr', y='DpT', hue='Alley', ax=ax)
        ax.set_title(f"Deaths per tornado in the years 1970-2023, per year")
        ax.set_xlabel("year")
        ax.set_ylabel("number of fatalities per tornado")

        return fig




st.header('Dixie Alley the new Tornado Alley?')
st.write('Did you know that Tornado Alley is shifting east?')
st.write("Tornado Alley doesn't have a set boundary, but it traditionally includes states like \
         Texas, Oklahoma, Kansas, and Nebraska.  This may also include other states like \
         Missouri or Iowa; its not fixed.  But there's a new player in the town of tornados, and \
         thats Dixie Alley.")
st.write("Dixie Alley contains states like Louisiana, Arkansas, Mississippi, Alabama, Georgia, \
         and Tennessee.  This area has been rising in tornados, rivaling the old \
         Tornado Alley.  By using visualizations found in our website, you can confirm this yourself!")
st.write("Take a look below to see some tornado visualizations")

test = Alley(df)
st.pyplot(test.alley_freq())

st.write("Dixie Alley looks to have started eclipsing the tornado frequency of Tornado Alley \
         around 2005.")
st.pyplot(test.alley_deaths())
st.pyplot(test.alley_injuries())

st.write("Interestingly, it doesn't appear, besides the exception of 2011, that deaths or injuries \
         appear to rise in the same dramatic fashion that the frequency of tornados has increased.  \
         In fact, death per tornado in Dixie Alley seems to be higher from the get go.  Lets explore this")

st.pyplot(test.death_per_tornado())

st.write("It appears to be so that tornados are more deadly in Dixie Alley than Tornado Alley, and it \
         looks like that's been a theme well before tornado frequency increased.  Why does that happen?")
st.write("We can't tell you why, but we can help you visualize information better than any other website \
         available to you!  See our 'Discovery' page to learn more about tornados.  When you see \
         something interesting or unusual, use that as a starting point to continue your interest with \
         further external research.")