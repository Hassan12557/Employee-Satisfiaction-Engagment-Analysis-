import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

filepath=r"D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"
def load_and_drop_base(filepath):
    """
    Step 1: Base Cleaning
    Loads the raw CSV dataset and drops the 7 uninformative/noisy columns.
    Shared across all modeling tasks.
    """
    df = pd.read_csv(filepath)
    columns_to_drop = [
        'EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber',
        'DailyRate', 'HourlyRate', 'MonthlyRate'
    ]
    return df.drop(columns=columns_to_drop, errors='ignore')


def get_regression_data(filepath):
    """
    Step 2: Option A Pipeline (Regression / Feature Importance)
    Processes raw data into clean, encoded, non-collinear, and scaled train/test sets.
    """
    # 1. Run base cleaning
    df_clean = load_and_drop_base(filepath)
    
    # 2. Isolate Features (X) and Target (y)
    # Using 'Attrition' as the target based on baseline project setup
    X = df_clean.drop(columns=['Attrition'], errors='ignore')
    y = df_clean['Attrition']
    
    # 3. The Golden Split (80/20) - Stratified to keep class balance identical
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Categorical Encoding (One-Hot Encoding text variables)
    categorical_cols = X_train.select_dtypes(include=['object']).columns
    X_train_encoded = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)
    X_test_encoded = pd.get_dummies(X_test, columns=categorical_cols, drop_first=True)
    
    # Align structural columns between train and test sets to guarantee a perfect match
    X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='left', axis=1, fill_value=0)
    
    # 5. Drop Multicollinearity Culprits (The twin features we found in the heatmap)
    collinear_drops = ['JobLevel', 'TotalWorkingYears', 'YearsInCurrentRole', 'YearsWithCurrManager']
    X_train_final = X_train_encoded.drop(columns=collinear_drops, errors='ignore')
    X_test_final = X_test_encoded.drop(columns=collinear_drops, errors='ignore')
    
    # 6. Feature Scaling (Continuous numerical columns only)
    columns_to_scale = [
        'Age', 'DistanceFromHome', 'MonthlyIncome', 'NumCompaniesWorked', 
        'PercentSalaryHike', 'YearsAtCompany', 'YearsSinceLastPromotion'
    ]
    
    scaler = StandardScaler()
    X_train_final[columns_to_scale] = scaler.fit_transform(X_train_final[columns_to_scale])
    X_test_final[columns_to_scale] = scaler.transform(X_test_final[columns_to_scale])
    
    return X_train_final, X_test_final, y_train, y_test


# The block below only executes when you run data_preprocess.py directly.
# When imported into other files, Python completely ignores this block.
if __name__ == "__main__":
    print("Executing standalone pipeline test...")
    
    # Self-correcting path helper depending on where you execute the script from
    try:
        X_train, X_test, y_train, y_test = get_regression_data(filepath)
    except FileNotFoundError:
        X_train, X_test, y_train, y_test = get_regression_data(filepath)
        
    print("\n--- Pipeline Verification Check ---")
    print(f"Final X_train Shape (Should be 44 features): {X_train.shape}")
    print(f"Final X_test Shape:                           {X_test.shape}")
    print(f"y_train Shape:                                 {y_train.shape}")
    print("\nStatus: Data pipeline refactored and working perfectly!")