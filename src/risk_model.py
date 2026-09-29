# AI_Emergency_Intelligence_System\src\risk_model
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# -----------------------------
# File Paths
# -----------------------------
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
PROCESSED_PATH = os.path.join(BASE_PATH, "data_processed")
MODEL_PATH = os.path.join(BASE_PATH, "models")

os.makedirs(MODEL_PATH, exist_ok=True)

file_path = os.path.join(
    PROCESSED_PATH,
    "final_emergency_hourly_dataset.csv"
)

# -----------------------------
# Load Dataset
# -----------------------------
print("Loading dataset...")
df = pd.read_csv(file_path)

# -----------------------------
# Quantile-Based Risk Categorization
# -----------------------------
low_threshold = df["emergency_risk_score"].quantile(0.33)
high_threshold = df["emergency_risk_score"].quantile(0.66)

def categorize_risk(score):
    if score <= low_threshold:
        return "Low"
    elif score <= high_threshold:
        return "Medium"
    else:
        return "High"

df["risk_level"] = df["emergency_risk_score"].apply(categorize_risk)

# -----------------------------
# Feature Selection
# -----------------------------
features = [
    "crime_count",
    "crash_count",
    "PRCP",
    "TAVG",
    "is_peak_hour"
]

X = df[features]
y = df["risk_level"]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Train Random Forest
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt="d")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# -----------------------------
# Feature Importance
# -----------------------------
importances = model.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nFeature Importance:\n")
print(feature_importance_df)

plt.figure()
sns.barplot(
    x="Importance",
    y="Feature",
    data=feature_importance_df
)
plt.title("Feature Importance")
plt.show()

# -----------------------------
# Save Model
# -----------------------------
model_file = os.path.join(
    MODEL_PATH,
    "emergency_risk_model.pkl"
)

joblib.dump(model, model_file)

print("\nModel saved successfully 🚀")