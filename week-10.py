import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

tornado_df = pd.read_csv("D:/Gitprojects/Project/1950-2023_all_tornadoes.csv")

tornado_df['yr'] = pd.to_numeric(tornado_df['yr'], errors='coerce')

# Group data by 'yr' to sum up values per year
data_grouped = tornado_df.groupby('yr').sum().reset_index()

# Visualization 1: Total Injuries and Fatalities Over Time
plt.figure(figsize=(12, 6))
plt.plot(data_grouped['yr'], data_grouped['inj'], label='Total Injuries', color='blue', marker='o')
plt.plot(data_grouped['yr'], data_grouped['fat'], label='Total Fatalities', color='red', marker='o')
plt.title('Total Injuries and Fatalities Over Time')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.show()

# Visualization 2: Total Crop Loss and Property Loss Over Time
plt.figure(figsize=(12, 6))
plt.plot(data_grouped['yr'], data_grouped['closs'], label='Total Crop Loss', color='green', marker='o')
plt.plot(data_grouped['yr'], data_grouped['loss'], label='Total Property Loss', color='purple', marker='o')
plt.title('Total Crop Loss and Property Loss Over Time')
plt.xlabel('Year')
plt.ylabel('Loss Amount')
plt.legend()
plt.grid(True)
plt.show()