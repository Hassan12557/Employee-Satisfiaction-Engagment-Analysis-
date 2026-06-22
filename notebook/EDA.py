# 1. Load the dataset
# Replace 'WA_Fn-UseC_-HR-Employee-Attrition.csv' with your actual file name

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

# 2. Define categorical attributes for Pie Charts
categorical_attributes = [
    "Attrition",
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

# 3. Generate Individual Pie Charts in Sequence
print("Displaying categorical pie charts...")
for column in categorical_attributes:
    if column in df.columns:
        # Create a brand new individual window/figure
        plt.figure(figsize=(6, 6))

        # Calculate value distribution
        data_counts = df[column].value_counts()

        # Plot pie chart
        plt.pie(
            data_counts,
            labels=data_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=plt.cm.Pastel1.colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1},
        )
        plt.title(
            f"Distribution of {column}", fontsize=13, fontweight="bold", pad=15
        )
        plt.tight_layout()

        # Show this individual chart and pause until closed
        plt.show()
    else:
        print(f"Warning: Column '{column}' not found in the dataset.")

# 4. Generate the Individual Age Histogram
if "Age" in df.columns:
    print("Displaying Age histogram...")
    # Create an individual figure window for the histogram
    plt.figure(figsize=(8, 5))

    # Plot histogram with custom bins and borders
    plt.hist(
        df["Age"],
        bins=15,
        color="skyblue",
        edgecolor="black",
        alpha=0.8,
        rwidth=0.9,
    )

    # Add titles and labels
    plt.title("Distribution of Age", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Age", fontsize=11)
    plt.ylabel("Number of Employees", fontsize=11)

    # Add a subtle grid to make reading the frequency easier
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    # Show the final chart
    plt.show()
else:
    print("Warning: 'Age' column not found in the dataset.")

print("All charts have been displayed successfully!")