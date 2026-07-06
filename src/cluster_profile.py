import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
filepath=r"D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

try:
    from data_preprocess_and_visualization import get_clustering_data, load_and_drop_base
except ModuleNotFoundError:
    from data_preprocess_and_visualization import get_clustering_data, load_and_drop_base

# 1. Load scaled data for the model, and raw clean data for human readability
X_scaled = get_clustering_data(filepath)
df_readable = load_and_drop_base(filepath)

# 2. Train the Final K-Means Model using our optimal K=3
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, init='k-means++', random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

# 3. Attach the group numbers back to our readable dataset
df_readable['Employee_Segment'] = cluster_labels

print(f"=== Workforce Segmentation Complete (K={optimal_k}) ===")
print(df_readable['Employee_Segment'].value_counts().sort_index())
print("===============================================\n")

# 4. Profile the core differences between these groups
# We look at key metrics: Age, Income, Experience, and how much they travel/work overtime
profiling_cols = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'PercentSalaryHike']
profile = df_readable.groupby('Employee_Segment')[profiling_cols].mean()

# Add categorical behavior checks for each group
profile['OverTime_Rate'] = df_readable.groupby('Employee_Segment')['OverTime'].apply(lambda x: (x == 'Yes').mean() * 100)
profile['Frequent_Travel_Rate'] = df_readable.groupby('Employee_Segment')['BusinessTravel'].apply(lambda x: (x == 'Travel_Frequently').mean() * 100)

print("--- Employee Segment Profiles (Averages) ---")
print(profile.round(1).to_string())