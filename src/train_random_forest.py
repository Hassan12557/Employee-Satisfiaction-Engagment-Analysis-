import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
filepath=r"D:\Data Science Projects\Employee-Satisfaction-Engagement-Analysis\Data\IBM-HR.csv"

# 1. Import your data pipeline
try:
    from data_preprocess_and_visualization import get_classification_data
except ModuleNotFoundError:
    from data_preprocess_and_visualization import get_classification_data

print("Loading 37-feature dataset for Tree-Based Classification...")
X_train, X_test, y_train, y_test = get_classification_data(filepath)

# 2. Initialize and train the Random Forest Classifier
# We use class_weight='balanced' to handle the ~16% minority attrition class
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# 3. Predict and Evaluate
y_pred = rf_model.predict(X_test)
y_proba = rf_model.predict_proba(X_test)[:, 1]

print("\n================ RANDOM FOREST PERFORMANCE ================")
print(classification_report(y_test, y_pred))
print(f"Random Forest ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
print("===========================================================\n")

# 4. Extract Feature Importances (Mean Decrease in Impurity)
importances = rf_model.feature_importances_
rf_importance = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("Top 10 Most Important Features (Tree Splits):")
print(rf_importance.head(10).to_string(index=False))

# 5. Plot Random Forest Feature Importance
plt.figure(figsize=(12, 8))
sns.barplot(
    x='Importance',
    y='Feature',
    data=rf_importance.head(15),
    palette='viridis',
    hue='Feature',
    legend=False
)
plt.title("Random Forest: Top 15 Feature Importances", fontsize=16, fontweight='bold')
plt.xlabel("Importance Score (Mean Decrease in Impurity)", fontsize=12)
plt.ylabel("Features", fontsize=12)
plt.tight_layout()
plt.show()