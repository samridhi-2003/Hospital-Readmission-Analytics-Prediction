
# Hospital Readmission Analytics & Prediction System

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
