import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split

# 1. Load the dataset
csv_filename = "D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

if not os.path.exists(csv_filename):
    print(
        f"Error: '{csv_filename}' not found. Please make sure the file is in the same directory."
    )
    exit()

df = pd.read_csv(csv_filename)
print(f"Original dataset shape: {df.shape}")

# Create a case-insensitive, space-insensitive mapping of the actual CSV columns
csv_column_lookup = {col.lower().replace(" ", ""): col for col in df.columns}

# 2. Check for missing values
print("\n--- Missing Values Count per Column ---")
missing_summary = df.isnull().sum()
print(missing_summary[missing_summary > 0])
if missing_summary.sum() == 0:
    print("Good news! There are no missing values in this dataset.")

# 3. Drop uninformative / noisy columns
columns_to_drop_raw = [
    "EmployeeCount",
    "Over18",
    "StandardHours",
    "EmployeeNumber",
    "DailyRate",
    "HourlyRate",
    "MonthlyRate",
    "JobLevel",
    "YearsInCurrentRole",
    "YearsWithCurrManager"
]

# Match exact column names from the CSV file using our lookup dictionary
actual_drops = [
    csv_column_lookup[col.lower()]
    for col in columns_to_drop_raw
    if col.lower() in csv_column_lookup
]
df_cleaned = df.drop(columns=actual_drops, errors="ignore")
print(f"Dropped uninformative columns. Cleaned shape: {df_cleaned.shape}")

# Re-build lookup dictionary for the remaining columns
csv_column_lookup = {
    col.lower().replace(" ", ""): col for col in df_cleaned.columns
}

# 4. Apply One-Hot Encoding to requested categorical columns
categorical_to_encode_raw = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

# Map to actual column names in the dataset
actual_categorical = [
    csv_column_lookup[col.lower().replace(" ", "")]
    for col in categorical_to_encode_raw
    if col.lower().replace(" ", "") in csv_column_lookup
]

print(f"\nApplying One-Hot Encoding to: {actual_categorical}")
# dtype=int converts the resulting True/False boolean flags into clean 1s and 0s
df_encoded = pd.get_dummies(
    df_cleaned, columns=actual_categorical, dtype=int, drop_first=False
)
print(f"Dataset shape post-One-Hot Encoding: {df_encoded.shape}")

# 5. Separate Features (X) and Target Variable (y)
target_key = "attrition"
if target_key in csv_column_lookup:
    actual_target = csv_column_lookup[target_key]
    X = df_encoded.drop(columns=[actual_target])
    y = df_encoded[actual_target].map({"Yes": 1, "No": 0})
else:
    print(f"Critical Error: Target column 'Attrition' not found.")
    exit()

# 6. Split into Training and Testing Sets (80/20 Split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n--- Data Split Summary ---")
print(f"Training Features Shape (X_train): {X_train.shape}")
print(f"Testing Features Shape (X_test):   {X_test.shape}")

# 7. Correlation Analysis (TRAINING SET ONLY)
print("\nGenerating Correlation Matrix for the Training Set...")

# Recombine training features with training labels to view direct correlations
X_train_numeric = X_train.copy()
X_train_numeric["Attrition"] = y_train

# Compute correlation matrix
corr_matrix = X_train_numeric.corr()

# Isolate the correlation of all features specifically against Attrition
attrition_corr = corr_matrix[["Attrition"]].sort_values(
    by="Attrition", ascending=False
)

# Plot an optimized heatmap targeting Attrition relationships
plt.figure(figsize=(6, 15))
sns.heatmap(
    attrition_corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    vmin=-1,
    vmax=1,
    cbar_kws={"label": "Correlation Coefficient"},
)

plt.title(
    "Features vs Attrition Churn Correlation\n(Training Set Only)",
    fontsize=12,
    fontweight="bold",
    pad=15,
)
plt.tight_layout()
plt.show()

print("Pipeline executed successfully! Heatmap window displayed.")
