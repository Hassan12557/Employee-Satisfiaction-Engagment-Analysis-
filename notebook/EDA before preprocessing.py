import os
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load the dataset
csv_filename = "D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

 
if not os.path.exists(csv_filename):
    print(
        f"Error: '{csv_filename}' not found. Please make sure the file is in the same directory."
    )
    exit()

df = pd.read_csv(csv_filename)

# Create a case-insensitive, space-insensitive mapping of the actual CSV columns
# This ensures columns like 'Dailyrate' or 'jobsatisfication' match correctly.
csv_column_lookup = {col.lower().replace(" ", ""): col for col in df.columns}

# 2. Define Categorical Attributes for Pie Charts
categorical_requests = [
    "Attrition",
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

# 3. Define Numerical / Discrete Attributes for Histograms
numerical_requests = [
    "Age",
    "DailyRate",
    "DistanceFromHome",
    "Education",
    "EmployeeCount",
    "EmployeeNumber",
    "EnvironmentSatisfaction",
    "HourlyRate",
    "JobInvolvement",
    "JobLevel",
    "JobSatisfaction",
    "MonthlyIncome",
    "MonthlyRate",
    "NumCompaniesWorked",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
    "StandardHours",
    "StockOptionLevel",
    "TotalWorkingYears",
    "TrainingTimesLastYear",
    "WorkLifeBalance",
    "YearsAtCompany",
    "YearsInCurrentRole",
    "YearsSinceLastPromotion",
    "YearsWithCurrManager",
]

# --- PHASE 1: SEQUENTIAL PIE CHARTS ---
print("Starting Categorical Pie Charts processing...")
for req_name in categorical_requests:
    lookup_key = req_name.lower().replace(" ", "")

    if lookup_key in csv_column_lookup:
        actual_column = csv_column_lookup[lookup_key]

        # Create individual window
        plt.figure(figsize=(6, 6))
        data_counts = df[actual_column].value_counts()

        plt.pie(
            data_counts,
            labels=data_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.Pastel1.colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1},
        )
        plt.title(
            f"Distribution of {actual_column}",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )
        plt.tight_layout()

        # Display individual plot and halt until closed
        plt.show()
    else:
        print(f"Warning: Could not find categorical column matching '{req_name}'")


# --- PHASE 2: SEQUENTIAL HISTOGRAMS ---
print("\nStarting Numerical Histograms processing...")
for req_name in numerical_requests:
    lookup_key = req_name.lower().replace(" ", "")

    if lookup_key in csv_column_lookup:
        actual_column = csv_column_lookup[lookup_key]

        # Create individual window
        plt.figure(figsize=(8, 5))

        # Dynamically set bins if the feature is low-cardinality discrete data (like Education or JobLevel)
        unique_vals = df[actual_column].nunique()
        num_bins = min(unique_vals, 15) if unique_vals > 1 else 5

        # Plot Histogram
        plt.hist(
            df[actual_column],
            bins=num_bins,
            color="skyblue",
            edgecolor="black",
            alpha=0.8,
            rwidth=0.9 if unique_vals < 10 else 1.0,
        )

        # Style updates
        plt.title(
            f"Distribution of {actual_column}",
            fontsize=14,
            fontweight="bold",
            pad=15,
        )
        plt.xlabel(actual_column, fontsize=11)
        plt.ylabel("Number of Employees", fontsize=11)
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()

        # Display individual plot and halt until closed
        plt.show()
    else:
        print(f"Warning: Could not find numerical column matching '{req_name}'")

print("\nAll interactive visualizations completed successfully!")