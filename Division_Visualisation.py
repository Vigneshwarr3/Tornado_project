import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

class DivisionVis:
    def __init__(self, df, division, start_year, end_year):
        self.df = df
        self.division = division
        self.years = [start_year, end_year]

    ''' INFLATION ADJUSTED LOSSES '''

    # df is cleaned tornado, region is array ['x','y','z'], years is [start,end]
    def infl_adj_loss_division(self):
        self.df['loss_adjusted'] = self.df['damage'] * self.df['CPI_Multiplier']
        new_df = self.df[self.df['Division'].isin(self.division)]
        new_df = new_df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('Division')['loss_adjusted'].sum().reset_index()
        
        ax = sns.barplot(data = group_df.iloc[0:10], x = 'Division', y = 'loss_adjusted')
        labels = [textwrap.fill(label.get_text(), 12) for label in ax.get_xticklabels()]
        plt.title(f"Inflation for regions btw {self.years[0]} - {self.years[1]}")
        ax.set_xticklabels(labels)
        plt.ylabel("dollar loss, inflation adjusted for 8/24") 

        return plt
    
    def fat_division(self):
        new_df = self.df[self.df['Division'].isin(self.division)]
        new_df = new_df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        group_df = new_df.groupby('Division')['fat'].sum().reset_index()
        
        fig, ax = plt.subplots()
        axs = sns.barplot(data = group_df.iloc[0:10], x = 'Division', y = 'fat', ax=ax)
        labels = [textwrap.fill(label.get_text(), 12) for label in axs.get_xticklabels()]
        ax.set_title(f"Total fatalities for Divisions in the years {self.years[0]} - {self.years[1]}")
        ax.set_xticklabels(labels)
        ax.set_ylabel("fatalities") 

        return fig