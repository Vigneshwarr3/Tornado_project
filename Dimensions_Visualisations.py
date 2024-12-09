import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

class DimensionsVis:
    def __init__(self, df, states, start_year, end_year):
        self.df = df
        self.states = states
        self.years = [start_year, end_year]

    # Function to format y-axis values
    def format_yaxis(self, value, tick_number):
        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.0f}B"
        elif value >= 1_000_000:
            return f"{value/1_000_000:.0f}M"
        elif value >= 1_000:
            return f"{value/1_000:.0f}K"
        else:
            return str(int(value))

    ''' INFLATION ADJUSTED LOSSES '''

    # df is cleaned tornado, region is array ['x','y','z'], years is [start,end]
    def tornado_width_over_time(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=new_df, x="yr", y="wid", errorbar=None)
        plt.title('Trend in Tornado Width (Yards) Over Time')
        plt.ylabel('Width (Yards)')
        plt.xlabel('Year')

        return plt
    
    def tornado_length_over_time(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        
        plt.figure(figsize=(10, 4))
        sns.lineplot(data=new_df, x="yr", y="len", errorbar=None)
        plt.title('Trend in Tornado Length (Miles) Over Time')
        plt.ylabel('Length (Miles)')
        plt.xlabel('Year')

        return plt
    
    def magnitude_vs_fatalities(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[self.df['yr'].isin(list(range(int(self.years[0]),int(self.years[1]) ))) ]
        
        plt.figure(figsize=(10, 4))
        sns.scatterplot(data=new_df, x="mag", y="fat", alpha=0.6)
        plt.title('Tornado Magnitude vs Fatalities')
        plt.ylabel('Fatalities')
        plt.xlabel('Magnitude (F-Scale)')   
        
        return plt
    
    def visualize_high_intensity_tornadoes(self):
        new_df = self.df[self.df['State'].isin(self.states)]
        new_df = new_df[new_df['yr'].isin(list(range(int(self.years[0]), int(self.years[1]))))]
        
        high_intensity_tornadoes = new_df[new_df['mag'] >= 3]

        state_stats = high_intensity_tornadoes.groupby('State').agg(
            avg_width=('wid', 'mean'),
            avg_length=('len', 'mean')
        ).reset_index()
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))  
     
        sns.barplot(data=state_stats, x='State', y='avg_width', ax=axes[0], palette='viridis', errorbar=None)
        axes[0].set_title('Average Width of EF3 and Above Tornadoes by State')
        axes[0].set_xlabel('State')
        axes[0].set_ylabel('Average Width (yards)')
        axes[0].tick_params(axis='x', rotation=90)

        sns.barplot(data=state_stats, x='State', y='avg_length', ax=axes[1], palette='magma', errorbar=None)
        axes[1].set_title('Average Length of EF3 and Above Tornadoes by State')
        axes[1].set_xlabel('State')
        axes[1].set_ylabel('Average Length (miles)')
        axes[1].tick_params(axis='x', rotation=90)

        fig.tight_layout()
        return plt
    
    
