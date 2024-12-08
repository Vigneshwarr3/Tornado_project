import pandas as pd
import matplotlib.pyplot as plt

def analyze_and_plot_tornado_seasonal_counts(dataframe):
    """
    Analyzes tornado data to compute seasonal tornado counts and visualize the results,
    without modifying the original DataFrame.
    
    Parameters:
    - dataframe (pd.DataFrame): A pandas DataFrame containing tornado data with a 'date' column and a 'Tornado Count' column.
    """
    # Convert 'date' column to datetime
    dataframe['date'] = pd.to_datetime(dataframe['date'])

    # Define a function to assign seasons based on the month
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'

    # Compute seasonal tornado counts dynamically
    seasonal_counts = (
        dataframe
        .assign(season=dataframe['date'].dt.month.map(get_season))  # Temporary 'season' column
        .groupby('season')['Tornado Count']
        .sum()
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

    # Show plot
    plt.tight_layout()
    plt.show()


analyze_and_plot_tornado_seasonal_counts(df)  
