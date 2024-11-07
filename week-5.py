import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


file_path = 'D:/Gitprojects/Project/1950-2023_all_tornadoes.csv'
tornado_data = pd.read_csv(file_path)

tornado_data.head()

max_intensity_by_state = tornado_data.groupby('st')['f1'].max().reset_index()

top_states = max_intensity_by_state.sort_values('f1', ascending=False).head(20)

plt.figure(figsize=(12, 8))
sns.barplot(data=top_states, x='st', y='f1', palette='viridis')
plt.title('Maximum Tornado Intensity by State (Top 20)')
plt.xlabel('State')
plt.ylabel('Maximum Tornado Intensity (F-Scale)')
plt.tight_layout()
plt.show()

sns.set(style="whitegrid")

# Visualization 1: Tornado Intensity vs Tornado Length
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tornado_data, x='f1', y='len', alpha=0.6)
plt.title('Tornado Intensity vs Length (Miles)')
plt.xlabel('Tornado Intensity (F-Scale)')
plt.ylabel('Tornado Length (Miles)')
plt.show()

# Visualization 2: Tornado Intensity vs Tornado Width
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tornado_data, x='f1', y='wid', alpha=0.6)
plt.title('Tornado Intensity vs Width (Yards)')
plt.xlabel('Tornado Intensity (F-Scale)')
plt.ylabel('Tornado Width (Yards)')
plt.show()