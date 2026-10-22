
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "data" / "hospital_cleaned.csv")

features = [
    "race",
    "gender",
    "age",
    "admission_type_id",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "A1Cresult",
    "diabetesMed"
]

X = df[features].copy()
y = df["readmitted_30d"].astype(int)

categorical_features = [
    "race",
    "gender",
    "age",
    "admission_type_id",
    "A1Cresult",
    "diabetesMed"
]

numerical_features = [
    col for col in features
    if col not in categorical_features
]

X[categorical_features] = (
    X[categorical_features]
    .replace("?", pd.NA)
    .astype("string")
    .fillna("Unknown")
    .astype(str)
)

X[numerical_features] = X[numerical_features].apply(
    pd.to_numeric, errors="coerce"
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]),
            numerical_features
        ),
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(
                    strategy="constant",
                    fill_value="Unknown"
                )),
                ("encoder", OneHotEncoder(
                    handle_unknown="ignore"
                ))
            ]),
            categorical_features
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}

model_dir = BASE_DIR / "models"
model_dir.mkdir(exist_ok=True)

for name, model in models.items():

    print(f"\nTraining {name}...")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
    print("Precision:", round(precision_score(y_test, y_pred, zero_division=0), 4))
    print("Recall:", round(recall_score(y_test, y_pred, zero_division=0), 4))
    print("F1 Score:", round(f1_score(y_test, y_pred, zero_division=0), 4))
    print("ROC AUC:", round(roc_auc_score(y_test, y_prob), 4))

    filename = (
        "logistic_regression_model.pkl"
        if name == "Logistic Regression"
        else "random_forest_model.pkl"
    )

    joblib.dump(pipeline, model_dir / filename)

    print("Saved:", filename)

print("\nBoth models trained and saved successfully!")
