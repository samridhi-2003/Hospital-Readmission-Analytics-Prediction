
# Hospital Readmission Analytics & Prediction System


## Live Demo

# 🏥 Hospital Readmission Analytics & Prediction System

An end-to-end **Data Analytics, Data Warehousing, and Machine Learning project** that analyzes hospital readmission patterns and predicts the likelihood of patient readmission within 30 days.

The project integrates **Python, MySQL, Power BI, Scikit-learn, and Streamlit** to provide interactive analytics and a machine learning prediction system.

---

## 🚀 Live Demo

**Explore the Hospital Readmission Analytics & Prediction System:**

🔗 [Click Here to Open Live Application](https://hospital-readmission-analytics-prediction-7sy2bgz8fcpuagv7fwf5.streamlit.app)

---

## 📌 Project Overview

Hospital readmissions are an important healthcare quality indicator.

This project analyzes hospital encounter data to identify patterns associated with readmission and develops machine learning models to estimate the likelihood of readmission within 30 days.

### Project Objectives

- Clean and preprocess hospital encounter data.
- Build a MySQL data warehouse using a star schema.
- Perform SQL-based hospital readmission analysis.
- Develop an interactive Power BI dashboard.
- Train and evaluate machine learning classification models.
- Build a Streamlit web application for analytics and prediction.
- Deploy the application using Streamlit Community Cloud.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and machine learning |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| MySQL | Database management and data warehousing |
| Scikit-learn | Machine learning model development |
| Power BI | Business intelligence and visualization |
| Streamlit | Interactive web application |
| Plotly | Interactive charts and graphs |
| Joblib | Machine learning model serialization |
| Git & GitHub | Version control and project hosting |

---

## 📊 Dataset

**Dataset:** Diabetes 130-US Hospitals (1999–2008)

**Source:** UCI Machine Learning Repository

🔗 [UCI Diabetes Dataset](https://archive.ics.uci.edu/dataset/296/diabetes+130+us+hospitals+for+years+1999+2008)

### Dataset Information

| Attribute | Value |
|---|---|
| Total Records | 101,766 |
| Cleaned Dataset Columns | 50 |
| Target Variable | `readmitted_30d` |
| Readmission Within 30 Days | 11,357 |
| No Readmission Within 30 Days | 90,409 |
| 30-Day Readmission Rate | 11.16% |

### Target Variable

The target variable `readmitted_30d` is used for binary classification.

- **1:** Patient readmitted within 30 days.
- **0:** Patient not readmitted within 30 days, including readmissions after 30 days.

---

## ✨ Key Features

### 1. Data Cleaning and Preprocessing

- Handling missing values.
- Removing the `weight` column.
- Creating a binary target variable.
- Preparing categorical and numerical features.
- Generating a cleaned dataset for analysis.

### 2. MySQL Data Warehouse

- Star schema implementation.
- Seven dimension tables.
- One central fact table.
- Hospital admission and readmission analysis.
- SQL queries for data validation and reporting.

### 3. Power BI Dashboard

- Hospital readmission overview.
- Patient and admission analysis.
- Readmission trends.
- Interactive visualizations.
- Data-driven insights.

### 4. Machine Learning Prediction

Two classification algorithms are implemented:

- Logistic Regression
- Random Forest Classifier

The models estimate the likelihood of readmission within 30 days using patient and hospital encounter information.

### 5. Streamlit Web Application

The application includes:

- Interactive analytics dashboard.
- Patient information input form.
- Readmission prediction.
- Model performance comparison.
- Project information and documentation.

---

## 🗄️ SQL Database & Analytics

The project uses **MySQL** to store and analyze hospital readmission data using a star schema.

### Database Details

| Component | Description |
|---|---|
| Database | `hospital_dw` |
| Database System | MySQL |
| Schema Type | Star Schema |
| Fact Table | `Fact_Admission` |
| Dimension Tables | 7 |

### Dimension Tables

1. `Dim_Patient`
2. `Dim_Diagnosis`
3. `Dim_Admission_Type`
4. `Dim_Discharge`
5. `Dim_Admission_Source`
6. `Dim_Payer`
7. `Dim_Specialty`

### SQL Files

| File | Description |
|---|---|
| [P.sql](sql/P.sql) | Creates the database, dimension tables, and fact table |
| [Q.sql](sql/Q.sql) | Verifies record counts in database tables |
| [R.sql](sql/R.sql) | Performs SQL-based hospital readmission analysis |

### SQL Analytics

The SQL queries analyze:

- Overall hospital readmission rate.
- Readmission rate by patient age group.
- Readmission rate by admission type.
- Readmission rate by medical specialty.
- Readmission rate by hospital stay duration.
- Readmission rate by primary diagnosis.

---

## 🤖 Machine Learning Models

The project implements two supervised machine learning algorithms.

### Logistic Regression

A classification algorithm used to estimate the probability of readmission within 30 days.

### Random Forest

An ensemble learning algorithm that combines multiple decision trees for classification.

### Model Evaluation Results

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 67.41% | 68.34% |
| Precision | 17.03% | 17.54% |
| Recall | 49.63% | 49.67% |
| F1 Score | 25.36% | 25.93% |
| ROC AUC | 64.19% | 64.55% |

### Model Comparison

Random Forest achieved slightly better performance than Logistic Regression in the initial evaluation.

However, both models have relatively low precision and moderate recall, indicating that further improvements are required before considering any real-world application.

**Random Forest is used for prediction in the Streamlit demonstration application.**

---

## 🖥️ Streamlit Application Pages

### 🏠 Home

Provides an introduction to the Hospital Readmission Analytics & Prediction System.

### 📊 Analytics Dashboard

Displays interactive charts and hospital readmission statistics.

### 🧠 Readmission Prediction

Allows users to enter patient details and obtain a model-generated readmission risk estimate.

### 📈 Model Evaluation

Displays and compares the evaluation metrics of Logistic Regression and Random Forest.

### ℹ️ About Project

Provides information about the dataset, technologies, project objectives, and limitations.

---

## 📁 Project Structure

```text
Hospital_Readmission_Project/
│
├── data/
│   └── .gitkeep
│
├── models/
│   └── .gitkeep
│
├── sql/
│   ├── P.sql
│   ├── Q.sql
│   └── R.sql
│
├── streamlit_app/
│   ├── app.py
│   └── .streamlit/
│       └── config.toml
│
├── clean_data.py
├── train_model.py
├── etl.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Note:** The structure above shows the main project components. Local datasets and trained model files are excluded from GitHub.

---

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/samridhi-2003/Hospital-Readmission-Analytics-Prediction.git
```

### Step 2: Navigate to the Project Folder

```bash
cd Hospital-Readmission-Analytics-Prediction
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Prepare the Dataset

```bash
python clean_data.py
```

The script prepares the hospital dataset and generates:

```text
data/hospital_cleaned.csv
```

If the original dataset is unavailable locally, the script attempts to download it from the UCI Machine Learning Repository.

### Step 5: Train the Models

```bash
python train_model.py
```

This generates the trained machine learning models in the `models/` directory.

### Step 6: Run the Streamlit Application

From the project root directory:

```bash
python -m streamlit run streamlit_app/app.py
```

Open the local URL displayed in the terminal.

The application also attempts to prepare missing datasets and models automatically.

---

## 📈 Project Workflow

```text
UCI Hospital Dataset
        |
        v
Data Cleaning & Preprocessing
        |
        v
Cleaned Hospital Dataset
        |
        +----------------------+
        |                      |
        v                      v
MySQL Data Warehouse     Machine Learning
        |                      |
        v                      v
SQL Analytics           Model Evaluation
        |                      |
        v                      v
Power BI Dashboard      Readmission Prediction
                               |
                               v
                      Streamlit Web Application
                               |
                               v
                       Cloud Deployment
```

---

## 🔍 Key Insights

- The dataset contains 101,766 hospital encounters.
- Approximately 11.16% of encounters resulted in readmission within 30 days.
- SQL analysis enables comparison of readmission rates across patient and hospital encounter categories.
- Random Forest achieved a slightly higher ROC AUC and F1 score than Logistic Regression.
- Interactive dashboards make readmission patterns easier to explore.

---

## ⚠️ Limitations

- The machine learning models have limited predictive performance.
- Precision is relatively low, indicating a substantial number of false-positive predictions.
- The evaluation uses an encounter-level train-test split.
- Patient-level validation is recommended to reduce potential information leakage.
- Probability calibration and external validation are needed.
- The historical dataset may not represent current healthcare practices.

**Disclaimer:** This project is developed for educational and research demonstration purposes only. It is not intended for clinical diagnosis, treatment, or real-world medical decision-making.

---

## 🔮 Future Enhancements

- Improve model performance through feature engineering.
- Implement patient-level validation.
- Explore additional classification algorithms.
- Apply hyperparameter tuning.
- Improve probability calibration.
- Add model explainability using SHAP.
- Extend the analytics dashboard with additional visualizations.

---

## 👩‍💻 Author

**Samridhi Kumari**

B.Tech – Computer Science and Engineering  
Specialization: Data Science & Analytics  
DIT University, Dehradun

**GitHub:** [samridhi-2003](https://github.com/samridhi-2003)

---

## 🌐 Project Links

- **GitHub Repository:** [Hospital Readmission Analytics & Prediction](https://github.com/samridhi-2003/Hospital-Readmission-Analytics-Prediction)
- **Live Application:** [Streamlit Live Demo](https://hospital-readmission-analytics-prediction-7sy2bgz8fcpuagv7fwf5.streamlit.app)

---

⭐ If you find this project useful, consider starring the repository!

🚀 **Try the Hospital Readmission Analytics & Prediction System:**

[Click Here to Open Live Application](https://hospital-readmission-analytics-prediction-7sy2bgz8fcpuagv7fwf5.streamlit.app)


## Project Overview
An end-to-end Data Analytics and Machine Learning project
that analyzes hospital readmissions and estimates the
likelihood of readmission within 30 days.

## Technologies Used
- Python
- Pandas and NumPy
- MySQL
- Scikit-learn
- Power BI
- Streamlit
- Plotly

## Dataset
- Source: UCI Diabetes 130-US Hospitals Dataset
- Total Records: 101,766
- Total Columns: 50
- Target Variable: readmitted_30d
- 30-Day Readmission Rate: 11.16%

## Key Features
- Data Cleaning and ETL
- MySQL Data Warehouse with Star Schema
- Interactive Power BI Dashboard
- Streamlit Analytics Dashboard
- Patient Readmission Prediction Form
- Logistic Regression and Random Forest Models
- Machine Learning Model Evaluation

## Machine Learning Results

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 67.41% | 68.34% |
| Precision | 17.03% | 17.54% |
| Recall | 49.63% | 49.67% |
| F1 Score | 25.36% | 25.93% |
| ROC AUC | 64.19% | 64.55% |

Random Forest achieved slightly better performance
than Logistic Regression in the initial evaluation.

## Streamlit Application Pages
1. Home
2. Analytics Dashboard
3. Readmission Prediction
4. Model Evaluation
5. About Project

## Run the Application

Install dependencies:

```bash
python -m pip install pandas numpy scikit-learn joblib streamlit plotly
```

Start Streamlit:

```bash
cd streamlit_app
python -m streamlit run app.py
```

## Limitations
The ML models have limited predictive performance.
Evaluation currently uses an encounter-level train-test
split. Patient-level validation and probability
calibration are recommended.

This project is for educational and research
demonstration purposes only and is not intended
for clinical decision-making.
