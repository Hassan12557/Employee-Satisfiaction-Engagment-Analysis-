import os
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load the dataset
# Replace 'WA_Fn-UseC_-HR-Employee-Attrition.csv' with your actual file name
csv_filename = "D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

if not os.path.exists(csv_filename):
    print(
        f"Error: '{csv_filename}' not found. Please make sure the file is in the same directory as this script."
    )
    exit()

df = pd.read_csv(csv_filename)

# 2. Define the attributes you want to plot
# Note: These match the standard full names from the IBM HR dataset.
# If your CSV uses the truncated names from your image preview (like 'Departme'), update them here.
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

# 3. Initialize a 4x2 grid of subplots for the 8 features
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(14, 20))
axes = axes.flatten()  # Flatten into a 1D array to iterate easily

# 4. Generate pie charts dynamically
for i, column in enumerate(categorical_attributes):
    if column in df.columns:
        # Get data distribution counts
        data_counts = df[column].value_counts()

        # Plot pie chart on its respective subplot axis
        axes[i].pie(
            data_counts,
            labels=data_counts.index,
            autopct="%1.1f%%",  # Displays percentage values on slices
            startangle=140,
            colors=plt.cm.Pastel1.colors,  # Clean, readable palette
            wedgeprops={"edgecolor": "white", "linewidth": 1},
        )
        axes[i].set_title(
            f"Distribution of {column}", fontsize=13, fontweight="bold", pad=10
        )
    else:
        # Fallback error message inside the plot if a column name mismatch occurs
        axes[i].text(
            0.5,
            0.5,
            f"Column Not Found:\n'{column}'",
            ha="center",
            va="center",
            color="red",
            fontsize=12,
        )
        axes[i].axis("off")

# 5. Clean up layout formatting and show window
plt.tight_layout()
plt.show()
