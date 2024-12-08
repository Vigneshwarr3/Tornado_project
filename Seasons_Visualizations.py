import pandas as pd
import matplotlib.pyplot as plt

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