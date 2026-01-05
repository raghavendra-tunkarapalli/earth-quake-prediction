#train_model.py
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# LOAD DATA
df = pd.read_csv("usgs_earthquake_realistic_1000.csv")
df.columns = df.columns.str.strip()

X = df.drop(columns=["alert"], errors="ignore")
y = df["alert"]

# LABEL ENCODING
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# ---------- FEATURE ENGINEERING ----------
df["risk_score"] = (
    df["magnitude"] * 0.4 +
    (1 / (df["depth"] + 1)) * 20 +
    df["mmi"] * 3 +
    (df["sig"] / 100)
)

df["aftershock_probability"] = (
    df["magnitude"] / 10 +
    (1 / (df["depth"] + 1))
).clip(0, 1)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)


# PIPELINE (No scaling for tree models)
pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("model", RandomForestClassifier(class_weight="balanced", random_state=42))
])

# HYPERPARAMETER TUNING
params = {
    "model__n_estimators": [200, 300, 400],
    "model__max_depth": [10, 15, None],
    "model__min_samples_split": [2, 5, 10]
}

grid = GridSearchCV(
    pipeline,
    params,
    cv=5,
    scoring="f1_weighted",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

# EVALUATION
preds = best_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
print(classification_report(y_test, preds))


# SAVE MODEL & ENCODER
joblib.dump(best_model, "models/best_model.pkl")
joblib.dump(le, "models/label_encoder.pkl")

print("✅ Model & Label Encoder Saved Successfully")
