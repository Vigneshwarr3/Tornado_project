import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

file_path = 'd:/Gitprojects/Project/1950-2023_all_tornadoes.csv'  # Update the path if needed
tornado_data = pd.read_csv(file_path)

tornado_data['date'] = pd.to_datetime(tornado_data['date'])
tornado_data['year'] = tornado_data['date'].dt.year

#Tornado Width over Time
plt.figure(figsize=(10, 6))
sns.lineplot(data=tornado_data, x="year", y="wid", errorbar=None)
plt.title('Trend in Tornado Width (Yards) Over Time')
plt.ylabel('Width (Yards)')
plt.xlabel('Year')
plt.show()

#Tornado Length over Time
plt.figure(figsize=(10, 6))
sns.lineplot(data=tornado_data, x="year", y="len", errorbar=None)
plt.title('Trend in Tornado Length (Miles) Over Time')
plt.ylabel('Length (Miles)')
plt.xlabel('Year')
plt.show()

#Tornado Magnitude vs Fatalities
plt.figure(figsize=(8, 6))
sns.scatterplot(data=tornado_data, x="mag", y="fat", alpha=0.6)
plt.title('Tornado Magnitude vs Fatalities')
plt.ylabel('Fatalities')
plt.xlabel('Magnitude (F-Scale)')
plt.show()

high_intensity_tornadoes = tornado_data[tornado_data['mag'] >= 3]

# Group by state and calculate average width and length for high-intensity tornadoes
state_stats = high_intensity_tornadoes.groupby('st').agg(
    avg_width=('wid', 'mean'),
    avg_length=('len', 'mean')
).reset_index()

# Visualization: Bar plots for average tornado width and length in each state for EF3 and above tornadoes
fig, axes = plt.subplots(2, 1, figsize=(15, 14))

# Bar plot for average width
sns.barplot(data=state_stats, x='st', y='avg_width', ax=axes[0], hue='st', palette='viridis', legend=False)
axes[0].set_title('Average Width of EF3 and Above Tornadoes by State')
axes[0].set_xlabel('State')
axes[0].set_ylabel('Average Width (yards)')
axes[0].tick_params(axis='x', rotation=90)

# Bar plot for average length
sns.barplot(data=state_stats, x='st', y='avg_length', ax=axes[1], hue='st', palette='magma', legend=False)
axes[1].set_title('Average Length of EF3 and Above Tornadoes by State')
axes[1].set_xlabel('State')
axes[1].set_ylabel('Average Length (miles)')
axes[1].tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.show()


state_col = 'st'          
intensity_col = 'mag'     

central_states = ['TX', 'OK', 'KS', 'NE', 'SD', 'ND', 'IA', 'MO', 'AR', 'LA']
coastal_states = ['FL', 'GA', 'SC', 'NC', 'VA', 'MD', 'DE', 'NJ', 'NY', 'CT', 'RI', 'MA', 'ME', 
                  'CA', 'OR', 'WA', 'AL', 'MS']

# Filter the data for central and coastal states
central_data = tornado_data[tornado_data[state_col].isin(central_states)]
coastal_data = tornado_data[tornado_data[state_col].isin(coastal_states)]

# Drop rows with missing values in the intensity column
central_data_cleaned = central_data.dropna(subset=[intensity_col])
coastal_data_cleaned = coastal_data.dropna(subset=[intensity_col])

# Descriptive statistics
print("Central States Tornado Intensity Stats:")
print(central_data_cleaned[intensity_col].describe())

print("\nCoastal States Tornado Intensity Stats:")
print(coastal_data_cleaned[intensity_col].describe())

# Hypothesis testing: Independent t-test
t_stat, p_value = stats.ttest_ind(central_data_cleaned[intensity_col], coastal_data_cleaned[intensity_col])
print(f"\nT-test result: T-statistic = {t_stat}, P-value = {p_value}")

# Plotting the comparison
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.boxplot(x=state_col, y=intensity_col, data=tornado_data[tornado_data[state_col].isin(central_states + coastal_states)])
plt.title("Tornado Intensity Comparison between Central and Coastal States")
plt.xlabel("Region (Central or Coastal)")
plt.ylabel("Tornado Intensity (Fujita Scale)")
plt.show()

# Interpretation
if p_value < 0.05:
    print("There is a statistically significant difference in tornado intensity between central and coastal states.")
else:
    print("There is no statistically significant difference in tornado intensity between central and coastal states.")

yearly_counts = tornado_data['yr'].value_counts().sort_index()

# Plot the yearly tornado count
plt.figure(figsize=(14, 6))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o", color="b")
plt.title("Yearly Tornado Count (1950-2023)")
plt.xlabel("Year")
plt.ylabel("Number of Tornadoes")
plt.grid(True)
plt.show()

# Group by 'yr' and sum only the numeric columns
data_grouped = tornado_data.groupby('yr').sum(numeric_only=True).reset_index()


#Total Injuries and Fatalities Over Time
plt.figure(figsize=(12, 6))
plt.plot(data_grouped['yr'], data_grouped['inj'], label='Total Injuries', color='blue', marker='o')
plt.plot(data_grouped['yr'], data_grouped['fat'], label='Total Fatalities', color='red', marker='o')
plt.title('Total Injuries and Fatalities Over Time')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.show()

#Total Crop Loss and Property Loss Over Time
plt.figure(figsize=(12, 6))
plt.plot(data_grouped['yr'], data_grouped['closs'], label='Total Crop Loss', color='green', marker='o')
plt.plot(data_grouped['yr'], data_grouped['loss'], label='Total Property Loss', color='purple', marker='o')
plt.title('Total Crop Loss and Property Loss Over Time')
plt.xlabel('Year')
plt.ylabel('Loss Amount')
plt.legend()
plt.grid(True)
plt.show()