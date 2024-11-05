import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'd:/Gitprojects/Project/1950-2023_all_tornadoes.csv'  # Update the path if needed
tornado_data = pd.read_csv(file_path)

tornado_data['date'] = pd.to_datetime(tornado_data['date'])

tornado_data['year'] = tornado_data['date'].dt.year

sns.set(style="whitegrid")

# Visualization 1: Tornado Width over Time
plt.figure(figsize=(10, 6))
sns.lineplot(data=tornado_data, x="year", y="wid", errorbar=None)
plt.title('Trend in Tornado Width (Yards) Over Time')
plt.ylabel('Width (Yards)')
plt.xlabel('Year')
plt.show()

# Visualization 2: Tornado Length over Time
plt.figure(figsize=(10, 6))
sns.lineplot(data=tornado_data, x="year", y="len", errorbar=None)
plt.title('Trend in Tornado Length (Miles) Over Time')
plt.ylabel('Length (Miles)')
plt.xlabel('Year')
plt.show()


# Set up the plotting style
sns.set(style="whitegrid")

# Visualization 1: Tornado Magnitude vs Financial Loss
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tornado_data, x="mag", y="loss", alpha=0.6)
plt.title('Tornado Magnitude vs Financial Loss')
plt.ylabel('Financial Loss (Thousands of $)')
plt.xlabel('Magnitude (F-Scale)')
plt.show()

# Visualization 2: Tornado Magnitude vs Fatalities
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tornado_data, x="mag", y="fat", alpha=0.6)
plt.title('Tornado Magnitude vs Fatalities')
plt.ylabel('Fatalities')
plt.xlabel('Magnitude (F-Scale)')
plt.show()
