# 🏥 HealthGuardian AI – Intelligent Personalized Lifestyle Disease Risk Prediction System

**HealthGuardian AI** is a production-grade, AI-powered healthcare intelligence application that predicts lifestyle disease risks (Diabetes, Heart Disease, Hypertension, Obesity, Kidney Disease, Stroke), provides Explainable AI (SHAP & LIME) attributions, calculates 10 clinical body indicators, manages patient history in SQLite, and generates ReportLab PDF medical diagnostic reports.

---

## 🌟 Key Features

### 1. 🩸 Multi-Disease Risk Prediction Pipeline
- **6 Independent Lifestyle Disease Engines**:
  - **Diabetes Risk**: ML Ensemble on PIMA Dataset (XGBoost, CatBoost, Random Forest, Decision Tree, etc.).
  - **Heart Disease Risk**: Clinical ASCVD risk model.
  - **Hypertension Risk**: JNC-7 guideline classification.
  - **Obesity Risk**: WHO BMI & metabolic risk profiling.
  - **Kidney Disease Risk**: eGFR & glucose/BP risk screening.
  - **Stroke Risk**: Framingham Stroke Study algorithm.

### 2. 🤖 Automated 12-Model Trainer & Benchmarker
Trains, compares, and evaluates 12 Machine Learning classifiers:
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Extra Trees
5. Gradient Boosting
6. AdaBoost
7. XGBoost
8. LightGBM
9. CatBoost
10. K-Nearest Neighbors (KNN)
11. Support Vector Machine (SVM)
12. Naive Bayes

- **Automated Model Selection**: Automatically deploys the top-performing model based on validation Accuracy & F1 score.
- **Evaluation Metrics**: Accuracy, Precision, Recall, F1 Score, ROC-AUC, 5-Fold Cross Validation, and Confusion Matrix.

### 3. 🧠 Explainable AI (XAI)
- **SHAP (SHapley Additive exPlanations)**: Waterfall & Bar feature contribution charts.
- **LIME (Local Interpretable Model-agnostic Explanations)**: Local feature weight attribution for transparent clinical decision making.

### 4. 🧮 10 Interactive Health Calculators
- **BMI** (Body Mass Index)
- **Body Fat Percentage** (Deurenberg Formula)
- **Daily Water Intake**
- **Daily Calorie Target & Macro Breakdown**
- **Daily Protein Requirement**
- **Ideal Body Weight** (Devine Formula)
- **BMR** (Mifflin-St Jeor)
- **TDEE** (Total Daily Energy Expenditure)
- **WHR** (Waist-to-Hip Ratio)
- **BSA** (Body Surface Area - Mosteller Formula)

### 5. 💯 Composite Health Score Index
- Dynamic 0–100 score engine considering BMI, exercise, sleep, stress, water, smoking, alcohol, and disease prediction probabilities.
- Rendered via a Plotly Gauge Chart.

### 6. 🥗 Rule-Based AI Recommendation Engine
Generates tailored plans for:
- Diet & Nutrition
- Physical Exercise
- Hydration Schedule
- Sleep Hygiene
- Stress Management

### 7. 📄 ReportLab PDF Diagnostic Report
- Generates official PDF reports complete with Hospital Header, Patient Profile, Health Score, Multi-Disease Risk Matrix, AI Recommendations, QR Code Verification, and Medical Disclaimer.

### 8. 🔒 SQLite Authentication & Security
- Bcrypt password hashing (rounds=12).
- SQL Injection protection using parameterized queries.
- Admin Panel for user management & system audit logs.

### 9. 🎨 Modern Glassmorphism UI
- Blue Medical Theme with glass cards (`backdrop-filter: blur(12px)`).
- Dark Mode / Light Mode switcher.

---

## 📁 Modular Project Structure

```
HealthGuardian-AI/
├── app.py                      # Main Streamlit Application Entrypoint
├── requirements.txt            # Package dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore specs
├── assets/
│   └── style.css               # Glassmorphism CSS theme
├── auth/
│   ├── __init__.py
│   └── authenticator.py        # Bcrypt authentication & session state
├── database/
│   ├── __init__.py
│   ├── db_handler.py           # SQLite CRUD operations
│   └── healthguardian.db       # Auto-generated SQLite database
├── data/
│   └── diabetes.csv            # PIMA Diabetes Dataset
├── models/
│   ├── __init__.py
│   ├── pipeline.py             # Data preprocessing & feature engineering
│   ├── multi_model_trainer.py  # 12-model training & evaluation engine
│   ├── predictor.py            # 6 independent disease risk engines
│   ├── explainability.py       # SHAP & LIME visualization generators
│   └── saved_models/           # Saved model binaries (.pkl)
├── utils/
│   ├── __init__.py
│   ├── calculators.py          # 10 medical calculators
│   ├── health_score.py         # Composite health score & gauge chart
│   ├── ai_recommender.py       # Rule-based AI advice engine
│   ├── exporter.py             # CSV & Excel exporters
│   └── email_sender.py         # SMTP email helper
├── reports/
│   ├── __init__.py
│   └── pdf_generator.py        # ReportLab PDF builder
└── views/
    ├── __init__.py
    ├── home.py                 # Hero section & system stats
    ├── login_view.py           # Glassmorphism Login/Register portal
    ├── patient_profile.py      # Demographics & lifestyle manager
    ├── calculators_view.py     # Interactive health calculators
    ├── disease_prediction.py   # Multi-disease prediction & SHAP/LIME
    ├── analytics_dashboard.py  # Plotly interactive graphs
    ├── patient_history.py      # Prediction history manager & exports
    ├── admin_panel.py          # Admin user management console
    └── settings_view.py        # Theme & preference settings
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit, Custom HTML5/CSS3 (Glassmorphism), Streamlit Components
- **Machine Learning**: Scikit-Learn, XGBoost, LightGBM, CatBoost
- **Explainability**: SHAP, LIME
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly, Matplotlib
- **Database**: SQLite3
- **Security**: Bcrypt
- **PDF Generation**: ReportLab
- **Exports**: Openpyxl, CSV

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Kanya-888/HealthGuardian-AI-Intelligent-Personalized-Lifestyle-Disease-Risk-Prediction-System.git
cd HealthGuardian-AI-Intelligent-Personalized-Lifestyle-Disease-Risk-Prediction-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train ML Models (Optional - Auto-runs on app start)
```bash
python models/multi_model_trainer.py
```

### 4. Run Application
```bash
streamlit run app.py
```

---

## 📄 License
Distributed under the MIT License. Created by Palvadi Kanya Kusuma Priya.
