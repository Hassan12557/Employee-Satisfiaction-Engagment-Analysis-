import os
import pandas as pd
from sklearn.model_selection import train_test_split
# 1. Load your completely raw dataset
# (Replace 'your_raw_file.csv' with your actual file name)
csv_filename = "D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

df = pd.read_csv(csv_filename)

# 2. Check for missing values
print("\n--- Missing Values Count per Column ---")
missing_summary = df.isnull().sum()
print(missing_summary[missing_summary > 0])
if missing_summary.sum() == 0:
    print("Good news! There are no missing values in this dataset.")

# 3. Drop specified columns (Zero variance, redundant IDs, and synthetic noise)
columns_to_drop = [
    "EmployeeCount",  # Zero variance (always 1)
    "Over18",  # Zero variance (always Y)
    "StandardHours",  # Zero variance (always 80)
    "EmployeeNumber",  # Redundant/Useless random ID
    "DailyRate",  # Synthetic uniform noise
    "HourlyRate",  # Synthetic uniform noise
    "MonthlyRate",  # Synthetic uniform noise
]

# Using errors='ignore' ensures the script won't crash if a column was already dropped
df_cleaned = df.drop(columns=columns_to_drop, errors="ignore")
print(
    f"\nColumns dropped successfully. Cleaned dataset shape: {df_cleaned.shape}"
)

# 4. Separate Features (X) and Target Variable (y)
# 'Attrition' is our target label. We also map 'Yes'/'No' to 1/0 for machine learning compatibility.
target_column = "Attrition"

if target_column in df_cleaned.columns:
    X = df_cleaned.drop(columns=[target_column])
    y = df_cleaned[target_column].map({"Yes": 1, "No": 0})
else:
    print(f"Critical Error: Target column '{target_column}' not found.")
    exit()

# 5. Split into Training and Testing Sets
# - test_size=0.2 reserves 20% of the data for testing and 80% for training.
# - random_state=42 ensures the exact same split every time you run the code (reproducibility).
# - stratify=y ensures the target ratio (Yes vs No) remains identical across both train and test splits.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Verify the final splits
print("\n--- Data Split Summary ---")
print(f"Training Features Shape (X_train): {X_train.shape}")
print(f"Testing Features Shape (X_test):   {X_test.shape}")
print(f"Training Labels Shape (y_train):   {y_train.shape}")
print(f"Testing Labels Shape (y_test):     {y_test.shape}")

print(f"\nClass balance in Training Set:\n{y_train.value_counts(normalize=True)}")
print(f"Class balance in Testing Set:\n{y_test.value_counts(normalize=True)}")
print("\nData preprocessing and train-test split completed successfully!")