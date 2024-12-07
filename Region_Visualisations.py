import matplotlib.pyplot as plt
import seaborn as sns

class regionVis:
    def __init__(self, df, start_year, end_year):
        self.df = df
        self.years = [start_year, end_year]

    ''' INFLATION ADJUSTED LOSSES '''

    # df is cleaned tornado, region is array ['x','y','z'], years is [start,end]
    def infl_adj_loss_region(self):
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        new_df = self.df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('Region')['loss_adjusted'].sum().reset_index()
        
        sns.barplot(data = group_df.iloc[0:10], x = 'Region', y = 'loss_adjusted')
        plt.title(f"Inflation adjusted loss for regions btw {self.years[0]} - {self.years[1]}")
        plt.xlabel("Region")
        plt.ylabel("dollar loss, inflation adjusted for 8/24") 

        return plt
    
    def fat_region(self):
        new_df = self.df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('Region')['fat'].sum().reset_index()
        
        fig, ax = plt.subplots()
        sns.barplot(data = group_df.iloc[0:10], x = 'Region', y = 'fat', ax=ax)
        ax.set_title(f"Total fatalities for Regions in the years {self.years[0]} - {self.years[1]}")
        ax.set_xlabel("Region")
        ax.set_ylabel("fatalities") 

        return fig