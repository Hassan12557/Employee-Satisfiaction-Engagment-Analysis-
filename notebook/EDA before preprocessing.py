
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


# --- PHASE 3: TWO-VARIABLE ATTRITION ANALYSIS (WITH EXACT NUMBERS) ---
attrition_col = csv_column_lookup.get("attrition")

if attrition_col:
    # Target variables requested for deep-dive Attrition breakdown
    breakdown_requests = [
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

    print("\nStarting Bivariate Attrition Breakdowns...")
    for req_name in breakdown_requests:
        # Special Setup for Age to create customized age group blocks
        if req_name.lower() == "age":
            age_col = csv_column_lookup.get("age")
            if age_col:
                df["AgeGroup"] = pd.cut(
                    df[age_col],
                    bins=[0, 25, 35, 45, 55, 120],
                    labels=["Under 25", "25-34", "35-44", "45-54", "55+"],
                )
                target_col = "AgeGroup"
                display_label = "Age Group"
            else:
                continue
        else:
            lookup_key = req_name.lower().replace(" ", "")
            if lookup_key in csv_column_lookup:
                target_col = csv_column_lookup[lookup_key]
                display_label = target_col
            else:
                print(
                    f"Warning: Could not find cross-analysis column matching '{req_name}'"
                )
                continue

        # 1. Calculate the exact breakdown matrix
        crosstab_counts = pd.crosstab(df[target_col], df[attrition_col])

        # Print the exact numbers directly out to your PyCharm console log
        print(f"\n==========================================")
        print(f" EXACT COUNTS: Attrition vs {display_label}")
        print(f"==========================================")
        print(crosstab_counts)
        print("==========================================\n")

        # 2. Build the grouped comparison bar chart window
        fig, ax = plt.subplots(figsize=(10, 6))
        crosstab_counts.plot(
            kind="bar",
            ax=ax,
            color=["#a1c9f4", "#ff9f9b"],  # Blue for Stayed (No), Salmon for Left (Yes)
            edgecolor="black",
            width=0.75,
        )

        # 3. Label exact numbers on top of the bars dynamically
        for container in ax.containers:
            ax.bar_label(container, fmt="%d", label_type="edge", padding=4)

        # Polish layout styling
        ax.set_title(
            f"Employee Leave vs Stay Numbers by {display_label}",
            fontsize=14,
            fontweight="bold",
            pad=15,
        )
        ax.set_xlabel(display_label, fontsize=11)
        ax.set_ylabel("Number of Employees", fontsize=11)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")
        ax.legend(title="Attrition Status", labels=["No (Stayed)", "Yes (Left)"])
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout()
        plt.show()

        # Drop temporary column if created for AgeGroup
        if "AgeGroup" in df.columns:
            df.drop(columns=["AgeGroup"], inplace=True)

else:
    print(
        "Critical Error: 'Attrition' target column missing. Phase 3 skipped."
    )

print("\nAll data processing pipelines executed successfully!")