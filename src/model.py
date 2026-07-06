import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
filepath=r"D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

# 1. Import your automated regression data pipeline
try:
    from data_preprocess_and_visualization import get_regression_data
except ModuleNotFoundError:
    # Fallback in case your script name still has the old visualization text
    from data_preprocess_and_visualization import get_regression_data

print("Loading preprocessed datasets through the modular pipeline...")
X_train, X_test, y_train, y_test = get_regression_data(filepath)

# 2. Initialize and train the Logistic Regression Model
# We use class_weight='balanced' because our target (Attrition) is imbalanced (~16% vs ~84%)
model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 3. Evaluate the Model on the Testing Set
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n================ MODEL PERFORMANCE ACCURACY ================")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
print("============================================================\n")

# 4. Extract Feature Importance (Coefficients)
coefficients = model.coef_[0]
feature_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': coefficients,
    'Absolute_Value': np.abs(coefficients)
}).sort_values(by='Absolute_Value', ascending=False)

print("Top 10 Most Powerful Drivers of Attrition:")
print(feature_importance.head(10).to_string(index=False))

# 5. Plot the Top Feature Importances
plt.figure(figsize=(12, 8))
# Color code: Positive coefficients mean higher risk of leaving, negative means staying
colors = ['#ff6b6b' if c > 0 else '#4dadf7' for c in feature_importance['Coefficient']]

sns.barplot(
    x='Coefficient',
    y='Feature',
    data=feature_importance,
    palette=colors,
    hue='Feature',
    legend=False
)

plt.title("Feature Importance: Drivers of Employee Attrition", fontsize=16, fontweight='bold')
plt.xlabel("Coefficient Value (Impact Direction & Strength)", fontsize=12)
plt.ylabel("Features", fontsize=12)
plt.axvline(x=0, color='black', linestyle='--', linewidth=1)
plt.tight_layout()
plt.show()