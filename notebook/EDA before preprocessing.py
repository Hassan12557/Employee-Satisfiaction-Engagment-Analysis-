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
    "Over18",
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

# 4. Define specific attributes to break down strictly by Attrition status (Stay vs Leave)
attrition_breakdown_requests = [
    "Age",
    "BusinessTravel",
    "Department",
    "Education",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "Over18",
    "OverTime",
]


# --- PHASE 1: SEQUENTIAL PIE CHARTS ---
print("Starting Categorical Pie Charts processing...")
for req_name in categorical_requests:
    lookup_key = req_name.lower().replace(" ", "")
    if lookup_key in csv_column_lookup:
        actual_column = csv_column_lookup[lookup_key]

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
        plt.show()


# --- PHASE 2: SEQUENTIAL HISTOGRAMS ---
print("\nStarting Numerical Histograms processing...")
for req_name in numerical_requests:
    lookup_key = req_name.lower().replace(" ", "")
    if lookup_key in csv_column_lookup:
        actual_column = csv_column_lookup[lookup_key]

        plt.figure(figsize=(8, 5))
        unique_vals = df[actual_column].nunique()
        num_bins = min(unique_vals, 15) if unique_vals > 1 else 5

        plt.hist(
            df[actual_column],
            bins=num_bins,
            color="skyblue",
            edgecolor="black",
            alpha=0.8,
            rwidth=0.9 if unique_vals < 10 else 1.0,
        )
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
        plt.show()


# --- PHASE 3: DEEP DIVE - ATTRITION BREAKDOWN VISUALIZATIONS ---
print("\nStarting Attrition Cross-Tabulation Breakdown Charts...")
attrition_col = csv_column_lookup.get("attrition")

if attrition_col:
    for req_name in attrition_breakdown_requests:
        lookup_key = req_name.lower().replace(" ", "")

        if lookup_key in csv_column_lookup:
            actual_column = csv_column_lookup[lookup_key]

            # SPECIAL CASE: Age requires a grouped numerical histogram layout
            if lookup_key == "age":
                plt.figure(figsize=(10, 5))
                age_no = df[df[attrition_col] == "No"][actual_column]
                age_yes = df[df[attrition_col] == "Yes"][actual_column]

                plt.hist(
                    [age_no, age_yes],
                    bins=12,
                    color=["#a1c9f4", "#ff9f9b"],  # Soft Blue (Stay), Soft Red (Leave)
                    edgecolor="black",
                    label=["No (Stayed)", "Yes (Left)"],
                    rwidth=0.85,
                )
                plt.title(
                    f"Attrition Breakdown by {actual_column} Groups",
                    fontsize=14,
                    fontweight="bold",
                    pad=15,
                )
                plt.xlabel(actual_column, fontsize=11)
                plt.ylabel("Number of Employees", fontsize=11)
                plt.legend(title="Attrition", loc="upper right")
                plt.grid(axis="y", linestyle="--", alpha=0.4)
                plt.tight_layout()
                plt.show()

            # CATEGORICAL CASES: MaritalStatus, Department, OverTime, etc.
            else:
                # Create a cross-tabulation table of the variable vs Attrition
                crosstab_df = pd.crosstab(df[actual_column], df[attrition_col])

                # Plot side-by-side bars directly from the cross-tab data
                ax = crosstab_df.plot(
                    kind="bar",
                    figsize=(10, 6),
                    color=["#a1c9f4", "#ff9f9b"],
                    edgecolor="black",
                    width=0.7,
                )

                plt.title(
                    f"Attrition breakdown within {actual_column}",
                    fontsize=14,
                    fontweight="bold",
                    pad=15,
                )
                plt.xlabel(actual_column, fontsize=11)
                plt.ylabel("Number of Employees", fontsize=11)

                # Fix label overlap for variables with long text names (like JobRole)
                plt.xticks(rotation=30, ha="right", fontsize=10)
                plt.legend(
                    labels=["No (Stayed)", "Yes (Left)"],
                    title="Attrition Status",
                    loc="upper right",
                )
                plt.grid(axis="y", linestyle="--", alpha=0.4)
                plt.tight_layout()
                plt.show()
        else:
            print(
                f"Warning: Could not find target breakdown column for '{req_name}'"
            )
else:
    print("Error: Base 'Attrition' tracking column was not found in dataset.")

print("\nAll interactive visualizations completed successfully!")