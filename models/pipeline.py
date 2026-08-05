"""
Data Preprocessing & Feature Engineering Pipeline for HealthGuardian AI
Handles data cleaning, missing value imputation (median per outcome), outlier detection/clipping,
feature engineering, feature scaling, and train-test splits.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, RobustScaler

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "diabetes.csv")


def load_raw_data(data_path: str = DATA_PATH) -> pd.DataFrame:
    """Load the PIMA Diabetes Dataset."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    df = pd.read_csv(data_path)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset:
    1. Replace invalid 0 values in Glucose, BloodPressure, SkinThickness, Insulin, BMI with NaN.
    2. Impute NaNs with median grouped by Outcome.
    3. Perform Outlier clipping using IQR bounds.
    """
    df_clean = df.copy()

    # Features where 0 is physiologically invalid
    zero_invalid_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in zero_invalid_cols:
        df_clean[col] = df_clean[col].replace(0, np.nan)

    # Impute missing values with Outcome-specific median
    for col in zero_invalid_cols:
        if 'Outcome' in df_clean.columns:
            median_by_outcome = df_clean.groupby('Outcome')[col].transform('median')
            df_clean[col] = df_clean[col].fillna(median_by_outcome)
        else:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    # Outlier clipping using IQR
    for col in zero_invalid_cols + ['Age', 'DiabetesPedigreeFunction']:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)

    return df_clean


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered physiological domain features.
    """
    df_fe = df.copy()

    # Glucose to Insulin ratio (Insulin Sensitivity proxy)
    df_fe['Glucose_Insulin_Ratio'] = df_fe['Glucose'] / (df_fe['Insulin'] + 1.0)

    # BMI to Age ratio
    df_fe['BMI_Age_Interaction'] = df_fe['BMI'] * df_fe['Age'] / 100.0

    # Metabolic Syndrome Index (Combined Glucose + BP + BMI risk factor)
    df_fe['Metabolic_Risk_Index'] = (df_fe['Glucose'] / 100.0) * (df_fe['BloodPressure'] / 80.0) * (df_fe['BMI'] / 25.0)

    # High Blood Pressure Category (1 if BP > 80 else 0)
    df_fe['High_BP_Flag'] = (df_fe['BloodPressure'] >= 80).astype(int)

    # Obesity Class (1 if BMI >= 30 else 0)
    df_fe['Obesity_Flag'] = (df_fe['BMI'] >= 30.0).astype(int)

    return df_fe


def prepare_ml_dataset(data_path: str = DATA_PATH, test_size: float = 0.2, random_state: int = 42) -> Tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str], RobustScaler
]:
    """
    Complete dataset preparation pipeline returning scaled train/test arrays, feature names, and scaler.
    """
    df_raw = load_raw_data(data_path)
    df_clean = preprocess_data(df_raw)
    df_fe = engineer_features(df_clean)

    X = df_fe.drop(columns=['Outcome'])
    y = df_fe['Outcome'].values
    feature_names = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X.values, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names, scaler
