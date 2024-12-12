import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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
    plt.figure(figsize=(10, 4))
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

    # Convert losses to millions
    seasonal_losses_in_millions = seasonal_losses / 1_000_000

    # Plot losses by season
    plt.figure(figsize=(10, 5))
    plt.bar(seasonal_losses_in_millions.index, seasonal_losses_in_millions.values,
            color=['skyblue', 'orange', 'green', 'purple'], alpha=0.8)

    # Highlight the season with the highest loss
    max_loss_season = seasonal_losses_in_millions.idxmax()
    plt.bar(max_loss_season, seasonal_losses_in_millions[max_loss_season],
            color='red', alpha=0.8, label=f'Highest Loss ({max_loss_season})')

    # Add titles and labels
    plt.title('Tornado Losses by Season', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Total Loss (in Million)', fontsize=12)

    # Add legend
    plt.legend(fontsize=10)

    # Format y-axis to use "M" for millions
    def millions_formatter(x, _):
        return f'{int(x)}M' if x >= 1 else ''

    plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    # Aesthetic adjustments
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Show plot
    plt.tight_layout()

    # Show plot
    return plt


