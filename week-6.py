import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

file_path = 'd:/Gitprojects/Project/1950-2023_all_tornadoes.csv' 

# Read the dataset
tornado_data = pd.read_csv(file_path)

# Check the column names to confirm the presence of relevant columns
print("Column names in the dataset:", tornado_data.columns)

# Rename columns if necessary (update these based on the actual column names in your dataset)
if 'state' not in tornado_data.columns:
    tornado_data.rename(columns={'st': 'state'}, inplace=True)  # Update 'st' if the state column is named differently
if 'mag' not in tornado_data.columns:
    print("The 'mag' column could not be found. Please check your dataset for the correct column name.")

# Filter data for high-intensity tornadoes (EF3 and above)
high_intensity_tornadoes = tornado_data[tornado_data['mag'] >= 3]

# Group by state and calculate average width and length for high-intensity tornadoes
state_stats = high_intensity_tornadoes.groupby('state').agg(
    avg_width=('wid', 'mean'),
    avg_length=('len', 'mean')
).reset_index()

# Visualization: Bar plots for average tornado width and length in each state for EF3 and above tornadoes
fig, axes = plt.subplots(2, 1, figsize=(15, 14))

# Bar plot for average width
sns.barplot(data=state_stats, x='state', y='avg_width', ax=axes[0], hue='state', palette='viridis', legend=False)
axes[0].set_title('Average Width of EF3 and Above Tornadoes by State')
axes[0].set_xlabel('State')
axes[0].set_ylabel('Average Width (yards)')
axes[0].tick_params(axis='x', rotation=90)

# Bar plot for average length
sns.barplot(data=state_stats, x='state', y='avg_length', ax=axes[1], hue='state', palette='magma', legend=False)
axes[1].set_title('Average Length of EF3 and Above Tornadoes by State')
axes[1].set_xlabel('State')
axes[1].set_ylabel('Average Length (miles)')
axes[1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()
