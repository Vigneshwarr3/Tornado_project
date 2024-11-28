import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

file_path = "D:/Gitprojects/Project/1950-2023_all_tornadoes.csv"
data = pd.read_csv(file_path)

print(data.head())
print(data.info())

state_col = 'st'          
intensity_col = 'mag'     

central_states = ['TX', 'OK', 'KS', 'NE', 'SD', 'ND', 'IA', 'MO', 'AR', 'LA']
coastal_states = ['FL', 'GA', 'SC', 'NC', 'VA', 'MD', 'DE', 'NJ', 'NY', 'CT', 'RI', 'MA', 'ME', 
                  'CA', 'OR', 'WA', 'AL', 'MS']

# Filter the data for central and coastal states
central_data = data[data[state_col].isin(central_states)]
coastal_data = data[data[state_col].isin(coastal_states)]

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
sns.boxplot(x=state_col, y=intensity_col, data=data[data[state_col].isin(central_states + coastal_states)])
plt.title("Tornado Intensity Comparison between Central and Coastal States")
plt.xlabel("Region (Central or Coastal)")
plt.ylabel("Tornado Intensity (Fujita Scale)")
plt.show()

# Interpretation
if p_value < 0.05:
    print("There is a statistically significant difference in tornado intensity between central and coastal states.")
else:
    print("There is no statistically significant difference in tornado intensity between central and coastal states.")
