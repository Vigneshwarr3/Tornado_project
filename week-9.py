import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
file_path = 'D:/Gitprojects/Project/1950-2023_all_tornadoes.csv'
tornado_data = pd.read_csv(file_path)

# Display the first few rows and columns to understand the dataset structure and contents
tornado_data.head(), tornado_data.columns

# Set up visual style
sns.set(style="whitegrid")

# Group by year and count the number of tornadoes per year
yearly_counts = tornado_data['yr'].value_counts().sort_index()

# Plot the yearly tornado count
plt.figure(figsize=(14, 6))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o", color="b")
plt.title("Yearly Tornado Count (1950-2023)")
plt.xlabel("Year")
plt.ylabel("Number of Tornadoes")
plt.grid(True)
plt.show()
