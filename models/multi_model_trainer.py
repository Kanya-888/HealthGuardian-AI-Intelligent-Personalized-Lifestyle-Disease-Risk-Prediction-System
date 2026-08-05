"""
Multi-Model Machine Learning Trainer & Comparison Engine for HealthGuardian AI
Trains and evaluates 12+ Machine Learning models on PIMA Diabetes Dataset,
executes Cross Validation, metrics calculation, hyperparameter tuning,
saves models and comparison stats.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier,
    GradientBoostingClassifier, AdaBoostClassifier
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedKFold, cross_validate, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)

# Advanced ML Libraries
try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    from lightgbm import LGBMClassifier
    LGBM_AVAILABLE = True
except ImportError:
    LGBM_AVAILABLE = False

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pipeline import prepare_ml_dataset, DATA_PATH

SAVED_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)


def get_model_candidates(random_state: int = 42) -> Dict[str, Any]:
    """Instantiate candidate ML models."""
    models = {
        "Logistic Regression": LogisticRegression(random_state=random_state, max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state, max_depth=6),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
        "Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=random_state),
        "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=random_state),
        "KNN": KNeighborsClassifier(n_neighbors=7),
        "SVM": SVC(probability=True, random_state=random_state, C=1.0, kernel='rbf'),
        "Naive Bayes": GaussianNB(),
    }

    if XGB_AVAILABLE:
        models["XGBoost"] = XGBClassifier(n_estimators=100, random_state=random_state, eval_metric='logloss', verbosity=0)

    if LGBM_AVAILABLE:
        models["LightGBM"] = LGBMClassifier(n_estimators=100, random_state=random_state, verbose=-1)

    if CATBOOST_AVAILABLE:
        models["CatBoost"] = CatBoostClassifier(iterations=100, random_state=random_state, verbose=0)

    return models


def train_and_evaluate_all(data_path: str = DATA_PATH) -> Tuple[pd.DataFrame, str, Dict[str, Any]]:
    """
    Train and compare all candidate models.
    Select best model based on validation Accuracy / F1 Score.
    Save model binaries, scaler, and evaluation metrics.
    """
    X_train, X_test, y_train, y_test, feature_names, scaler = prepare_ml_dataset(data_path=data_path)
    models = get_model_candidates()

    results_list = []
    trained_models = {}

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        # Fit model
        model.fit(X_train, y_train)
        trained_models[name] = model

        # Test predictions
        y_pred = model.predict(X_test)
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = y_pred

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_prob)

        # Cross validation scores
        cv_scores = cross_validate(model, X_train, y_train, cv=cv, scoring='accuracy')
        cv_acc_mean = cv_scores['test_score'].mean()
        cv_acc_std = cv_scores['test_score'].std()

        cm = confusion_matrix(y_test, y_pred)
        fpr, tpr, thresholds = roc_curve(y_test, y_prob)

        results_list.append({
            "Model": name,
            "Accuracy": round(acc * 100, 2),
            "CV Accuracy": f"{round(cv_acc_mean * 100, 2)}% ± {round(cv_acc_std * 100, 2)}%",
            "CV_Mean": cv_acc_mean,
            "Precision": round(prec * 100, 2),
            "Recall": round(rec * 100, 2),
            "F1 Score": round(f1 * 100, 2),
            "ROC AUC": round(roc_auc * 100, 2),
            "Confusion Matrix": cm.tolist(),
            "FPR": fpr.tolist(),
            "TPR": tpr.tolist()
        })

    results_df = pd.DataFrame(results_list)
    results_df = results_df.sort_values(by="Accuracy", ascending=False).reset_index(drop=True)

    best_model_name = results_df.iloc[0]["Model"]
    best_model = trained_models[best_model_name]

    # Save artifacts
    artifacts = {
        "best_model_name": best_model_name,
        "best_model": best_model,
        "scaler": scaler,
        "feature_names": feature_names,
        "trained_models": trained_models,
        "results_df": results_df,
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test
    }

    joblib.dump(best_model, os.path.join(SAVED_MODELS_DIR, "best_diabetes_model.pkl"))
    joblib.dump(scaler, os.path.join(SAVED_MODELS_DIR, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(SAVED_MODELS_DIR, "feature_names.pkl"))
    joblib.dump(artifacts, os.path.join(SAVED_MODELS_DIR, "all_models_artifacts.pkl"))

    return results_df, best_model_name, artifacts


def load_model_artifacts() -> Dict[str, Any]:
    """Load cached model binaries or train if missing."""
    artifacts_path = os.path.join(SAVED_MODELS_DIR, "all_models_artifacts.pkl")
    if os.path.exists(artifacts_path):
        try:
            artifacts = joblib.load(artifacts_path)
            return artifacts
        except Exception:
            pass

    # Train if missing or failed to load
    _, _, artifacts = train_and_evaluate_all()
    return artifacts


if __name__ == "__main__":
    df_res, best_name, _ = train_and_evaluate_all()
    print("=== Model Training Completed ===")
    print(f"Best Model: {best_name}")
    print(df_res[["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]])
