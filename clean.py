import pandas as pd
import numpy as np
from datetime import timedelta, time, datetime

'''
CLEANING FUNCTIONS

Notes for cleaning functions are above each respective function, along with comments inside
group_tornados(df) needs to be called AFTER clean_col(df)
'''

'''
Cleaning Columns
INPUT: raw tornado df OR tornado df after external data has been merged
OUTPUT: the following cells are changed
- magnitude: old values are converted to estimated losses
- time: time values are updated (only a few errors)
- latitude and longitude: "0" end values are changed to start values
- The following are turned to N/A values for aggregation
    - loss/damage (0 => None)
    - closs (0 => NaN)
    - mag (0 => NaN)

Note: closs is not touched here.  If we include that data, it needs to be cleaned
'''
def clean_col(df):
    def loss_magnitude(df):
        # creates new column 'damage' that converts 'loss' to comparable amounts
        # see documentation for more info.  Converts old data to estimated dollar amounts

        df_d = df[['yr','loss']]

        row_d = []
        for x in range(df_d.shape[0]):
            loss = df_d['loss'][x]
            #fixes problem from 1996-2015
            if(loss == 0):
                row_d.append(None)
                continue
            elif(df_d['yr'][x] >= 2016):
                row_d.append(loss)
                continue
            elif(df_d['yr'][x] >= 1996):
                loss = loss * 1000000 
                row_d.append(loss)
                continue
            else:
                loss = 5 * (10**(loss + 0.5))
                row_d.append(loss)
                continue

        df['damage'] = row_d
        return df
    
    def change_time(df):
        df['tz'].replace(0, np.nan, inplace=True)
        # since its one value I'm just doing this
        # I couldn't figure out how to subtract 5 hours without formatting issues
        df.loc[df['tz'] == 9, 'time'] = '02:08:00'
        return df
    
    def latlon(df):
        # replaces 0 values with starting location for mapping purposes
        df.loc[df['elat'] == 0, 'elat'] = df['slat']
        df.loc[df['elon'] == 0, 'elon'] = df['slon']
        return df
    
    # makes dollar estimate for old data
    df = loss_magnitude(df)
    # changes bad time info
    df = change_time(df)
    # updates latitude and longitude for plotting
    df = latlon(df)
    # updates missing values as NA so agg functions work
    df['mag'].replace(-9, np.nan, inplace=True)
    df['closs'].replace(0, np.nan, inplace=True)
    
    return df
    
'''
Cleaning Rows
INPUT: tornado df after columns have been cleaned
OUTPUT: tornados are grouped together, each row is now its own tornado
A few things to note...
- closs is commented out since no clean has been done. If clean is done, we can add
- this isn't great for tornados that cross state lines... yeah
'''
def group_tornado(df):
    # creates new column that combines om and yr
    # this creates a unique value for each tornado that can be grouped by
    df['ut'] = df['om'].astype(str) + df['yr'].astype(str)
    
    tornados = df.groupby(by=['ut']).agg({
        'yr': 'min',
        'mo': 'min',
        'dy': 'min',
        'date': 'min',
        'time': 'min',
        'st': 'max', #idk about this one but it returns something
        'mag': 'max',
        'inj': 'sum',
        'fat': 'sum',
        'damage': 'sum',
        #'closs': 'sum',
        'slat': 'max',
        'slon': 'max',
        'elat': 'max',
        'elon': 'max',
        'len': 'sum',
        'wid': 'max',
        'fc': 'max',
        'CPI_Multiplier': 'max',
        'pop': 'max',
        'Total area': 'max',
        'Land area': 'max',
        'Water area': 'max'
    })
    return tornados