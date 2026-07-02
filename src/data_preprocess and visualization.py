import os
import pandas as pd
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
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

# --- PHASE 6: CORRELATION ANALYSIS ON TRAINING SET ONLY ---
print("\nGenerating Correlation Matrix for the Training Set...")

# 1. Select only numerical features from the training set
X_train_numeric = X_train.select_dtypes(include=["number"]).copy()

# 2. Recombine numerical features with the training target (y_train)
# This lets you see exactly how each feature correlates with Attrition (0 or 1)
X_train_numeric["Attrition"] = y_train

# 3. Compute the Pearson correlation matrix
corr_matrix = X_train_numeric.corr()

# 4. Generate the Heatmap Plot Window
plt.figure(figsize=(14, 11))

# We use a diverging color map (coolwarm) to easily spot high positive/negative correlations
sns.heatmap(
    corr_matrix,
    annot=True,  # Displays exact correlation coefficients in the squares
    fmt=".2f",  # Rounds to 2 decimal places
    cmap="coolwarm",
    linewidths=0.5,
    vmin=-1,  # Minimum correlation value limit
    vmax=1,  # Maximum correlation value limit
    annot_kws={"size": 8},  # Scale down text inside squares for neatness
)

# Customize title and alignment configurations
plt.title(
    "Training Set Correlation Matrix (Features vs Attrition)",
    fontsize=16,
    fontweight="bold",
    pad=20,
)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Display the individual correlation window
plt.show()
print("Correlation matrix displayed successfully!")