import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# =====================================================
# STEP 1: LOAD DATASET
# =====================================================

data = pd.read_csv("dataset/diabetes.csv")

print("Dataset Shape:")
print(data.shape)


# =====================================================
# STEP 2: CLEAN DATA
# =====================================================

columns_to_clean = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]

for column in columns_to_clean:
    data[column] = data[column].replace(0, np.nan)

for column in columns_to_clean:
    data[column] = data[column].fillna(data[column].median())


# =====================================================
# STEP 3: FEATURES AND TARGET
# =====================================================

X = data.drop("Outcome", axis=1)
y = data["Outcome"]


# =====================================================
# STEP 4: TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# =====================================================
# STEP 5: FEATURE SCALING
# =====================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# =====================================================
# STEP 6: CREATE MODELS
# =====================================================

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ),

    "KNN":
        KNeighborsClassifier(n_neighbors=5),

    "SVM":
        SVC()
}


# =====================================================
# STEP 7: TRAIN MODELS
# =====================================================

results = {}

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")


for name, model in models.items():

    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    results[name] = {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

    print("\n" + name)

    print(
        "Accuracy :",
        round(accuracy * 100, 2),
        "%"
    )

    print(
        "Precision:",
        round(precision * 100, 2),
        "%"
    )

    print(
        "Recall   :",
        round(recall * 100, 2),
        "%"
    )

    print(
        "F1 Score :",
        round(f1 * 100, 2),
        "%"
    )


# =====================================================
# STEP 8: SELECT BEST MODEL
# =====================================================

best_model_name = max(
    results,
    key=lambda x: results[x]["f1"]
)

best_model = results[best_model_name]["model"]

print("\n==============================")
print("BEST MODEL")
print("==============================")

print("Model:", best_model_name)

print(
    "F1 Score:",
    round(
        results[best_model_name]["f1"] * 100,
        2
    ),
    "%"
)


# =====================================================
# STEP 9: FINAL PREDICTION
# =====================================================

y_pred = best_model.predict(X_test_scaled)


# =====================================================
# STEP 10: CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(y_test, y_pred)

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(cm)


# =====================================================
# STEP 11: CLASSIFICATION REPORT
# =====================================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =====================================================
# STEP 12: SAVE MODEL
# =====================================================

if not os.path.exists("model"):
    os.makedirs("model")


joblib.dump(
    best_model,
    "model/diabetes_model.pkl"
)

joblib.dump(
    scaler,
    "model/scaler.pkl"
)


print("\n==============================")
print("FILES SAVED")
print("==============================")

print("Model: model/diabetes_model.pkl")
print("Scaler: model/scaler.pkl")

print("\nTraining completed successfully!")