import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# Define a function to analyze and plot tornado counts by season
def plot_seasons(data):

    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'

    # Create a temporary column for season
    temp_season = data['date'].dt.month.apply(get_season)

    # Aggregate tornado counts by season
    seasonal_counts = (
        data.groupby(temp_season)['om']
        .nunique()
        .reindex(['Winter', 'Spring', 'Summer', 'Fall'])
    )

    # Plot tornado counts by season
    plt.figure(figsize=(8, 5))
    plt.bar(seasonal_counts.index, seasonal_counts.values, 
            color=['skyblue', 'orange', 'green', 'purple'], alpha=0.8)

    # Add titles and labels
    plt.title('Tornado Counts by Season', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Total Tornado Count', fontsize=12)

    # Aesthetic adjustments
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    return plt




# Define a function to analyze and plot tornado losses by season
def plot_loss_by_season(data):
    # Define seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'

    # Create a temporary column for season
    temp_season = data['date'].dt.month.apply(get_season)

    # Aggregate losses by season
    seasonal_losses = (
        data.groupby(temp_season)['loss']
        .sum()
        .reindex(['Winter', 'Spring', 'Summer', 'Fall'])
    )

    # Plot losses by season
    plt.figure(figsize=(8, 5))
    plt.bar(seasonal_losses.index, seasonal_losses.values,
            color=['skyblue', 'orange', 'green', 'purple'], alpha=0.8)

    # Highlight the season with the highest loss
    max_loss_season = seasonal_losses.idxmax()
    plt.bar(max_loss_season, seasonal_losses[max_loss_season],
            color='red', alpha=0.8, label=f'Highest Loss ({max_loss_season})')

    # Add titles and labels
    plt.title('Tornado Losses by Season', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Total Loss', fontsize=12)

    # Add legend
    plt.legend(fontsize=10)

    # Format y-axis to show values like 1,000, 2,000
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Aesthetic adjustments
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Show plot
    return plt


