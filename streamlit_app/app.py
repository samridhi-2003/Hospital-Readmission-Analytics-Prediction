import joblib
import plotly.express as px
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Hospital Readmission Analytics",
    page_icon="🏥",
    layout="wide",
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_DIR / "hospital_cleaned.csv")


ADMISSION_MAPPING = {
    1: "Emergency",
    2: "Urgent",
    3: "Elective",
    4: "Newborn",
    5: "Not Available",
    6: "Unknown",
    7: "Trauma Center",
    8: "Not Mapped",
}


def show_metrics(df):
    total_admissions = len(df)
    total_readmissions = int(df["readmitted_30d"].sum())
    readmission_rate = (100 * total_readmissions / total_admissions) if total_admissions else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏥 Total Admissions", f"{total_admissions:,}")
    with col2:
        st.metric("🔄 Total Readmissions", f"{total_readmissions:,}")
    with col3:
        st.metric("📈 Readmission Rate", f"{readmission_rate:.2f}%")


st.sidebar.title("🏥 Hospital Analytics")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Analytics Dashboard", "🧠 Readmission Prediction",
"📈 Model Evaluation","ℹ️ About Project"],
)
st.sidebar.markdown("---")
st.sidebar.info("Hospital Readmission Analytics & Prediction System")

if page == "🏠 Home":
    st.title("🏥 Hospital Readmission Analytics & Prediction System")
    st.markdown("### Welcome to the Hospital Analytics Dashboard")
    st.write(
        "An interactive healthcare analytics and machine learning application "
        "for analyzing hospital readmissions and predicting 30-day readmission risk."
    )
    st.divider()
    try:
        show_metrics(load_data())
    except (FileNotFoundError, pd.errors.EmptyDataError) as exc:
        st.error(f"Could not load the hospital dataset: {exc}")
    st.divider()
    st.success("Hospital Readmission Analytics System is running successfully!")

elif page == "📊 Analytics Dashboard":
    st.title("📊 Hospital Readmission Analytics Dashboard")
    try:
        df = load_data().copy()
    except (FileNotFoundError, pd.errors.EmptyDataError) as exc:
        st.error(f"Could not load the hospital dataset: {exc}")
        st.stop()

    required_columns = {
        "age", "gender", "admission_type_id", "readmitted_30d",
        "time_in_hospital", "medical_specialty",
    }
    missing = required_columns - set(df.columns)
    if missing:
        st.error("Missing dataset columns: " + ", ".join(sorted(missing)))
        st.stop()

    st.sidebar.subheader("🔍 Dashboard Filters")
    age_options = sorted(df["age"].dropna().unique().tolist())
    selected_ages = st.sidebar.multiselect("Select Age Group", age_options, default=age_options)
    df = df[df["age"].isin(selected_ages)].copy()

    gender_options = sorted(df["gender"].dropna().unique().tolist())
    selected_genders = st.sidebar.multiselect("Select Gender", gender_options, default=gender_options)
    df = df[df["gender"].isin(selected_genders)].copy()

    df["Admission Type"] = (
        pd.to_numeric(df["admission_type_id"], errors="coerce")
        .map(ADMISSION_MAPPING)
        .fillna("Unknown")
    )
    admission_options = sorted(df["Admission Type"].dropna().unique().tolist())
    selected_admissions = st.sidebar.multiselect(
        "Select Admission Type", admission_options, default=admission_options
    )
    df = df[df["Admission Type"].isin(selected_admissions)].copy()
    df["readmitted_30d"] = pd.to_numeric(df["readmitted_30d"], errors="coerce").fillna(0)

    st.subheader("📊 Hospital Readmission Overview")
    show_metrics(df)
    st.divider()
    st.success("Hospital dataset loaded successfully!")
    st.write("Total Records:", len(df))
    with st.expander("Dataset Preview"):
        st.dataframe(df.head(10), use_container_width=True)

    if df.empty:
        st.warning("No records match the selected filters. Please adjust the sidebar filters.")
        st.stop()

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 Age Group-wise Readmissions")
        age_data = (
            df.groupby("age", as_index=False)["readmitted_30d"]
            .sum()
            .sort_values("age")
        )
        fig_age = px.bar(
            age_data, x="age", y="readmitted_30d",
            title="Age Group-wise Readmissions",
            labels={"age": "Age Group", "readmitted_30d": "Total Readmissions"},
            color_discrete_sequence=["#7856B8"], text="readmitted_30d",
        )
        fig_age.update_traces(textposition="outside")
        fig_age.update_layout(xaxis_title="Age Group", yaxis_title="Total Readmissions")
        st.plotly_chart(fig_age, use_container_width=True)

    with chart_col2:
        st.subheader("👥 Gender-wise Readmissions")
        gender_data = (
            df.groupby("gender", as_index=False)["readmitted_30d"]
            .sum()
        )
        gender_data = gender_data[gender_data["readmitted_30d"] > 0]
        if gender_data.empty:
            st.info("No readmissions for the selected filters.")
        else:
            fig_gender = px.pie(
                gender_data, names="gender", values="readmitted_30d",
                title="Gender-wise Readmissions", hole=0.5,
                color_discrete_sequence=["#F472B6", "#3B82F6", "#A78BFA"],
            )
            fig_gender.update_traces(textinfo="percent+label", textposition="inside")
            st.plotly_chart(fig_gender, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        st.subheader("🏥 Hospital Stay-wise Readmissions")
        stay_data = (
            df.groupby("time_in_hospital", as_index=False)["readmitted_30d"]
            .sum()
            .sort_values("time_in_hospital")
        )
        fig_stay = px.bar(
            stay_data, x="time_in_hospital", y="readmitted_30d",
            title="Hospital Stay-wise Readmissions",
            labels={"time_in_hospital": "Hospital Stay (Days)",
                    "readmitted_30d": "Total Readmissions"},
            color_discrete_sequence=["#008C95"], text="readmitted_30d",
        )
        fig_stay.update_traces(textposition="outside")
        fig_stay.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis_title="Total Readmissions",
        )
        st.plotly_chart(fig_stay, use_container_width=True)

    with chart_col4:
        st.subheader("🚑 Admission Type-wise Readmissions")
        admission_data = (
            df.groupby("Admission Type", as_index=False)["readmitted_30d"]
            .sum()
            .sort_values("readmitted_30d", ascending=True)
        )
        fig_admission = px.bar(
            admission_data, x="readmitted_30d", y="Admission Type",
            orientation="h", title="Admission Type-wise Readmissions",
            labels={"readmitted_30d": "Total Readmissions"},
            color_discrete_sequence=["#7856B8"], text="readmitted_30d",
        )
        fig_admission.update_traces(textposition="outside")
        fig_admission.update_layout(
            xaxis_title="Total Readmissions", yaxis_title="Admission Type",
            margin=dict(l=20, r=65, t=60, b=40),
        )
        st.plotly_chart(fig_admission, use_container_width=True)

    st.subheader("🩺 Top 10 Medical Specialties by Readmissions")
    specialty_data = (
        df.assign(medical_specialty=df["medical_specialty"].fillna("Unknown"))
        .groupby("medical_specialty", as_index=False)["readmitted_30d"]
        .sum()
        .sort_values("readmitted_30d", ascending=False)
        .head(10)
        .sort_values("readmitted_30d", ascending=True)
    )
    fig_specialty = px.bar(
        specialty_data, x="readmitted_30d", y="medical_specialty",
        orientation="h", title="Top 10 Medical Specialties by Readmissions",
        labels={"readmitted_30d": "Total Readmissions",
                "medical_specialty": "Medical Specialty"},
        color_discrete_sequence=["#E879A8"], text="readmitted_30d",
    )
    fig_specialty.update_traces(textposition="outside")
    fig_specialty.update_layout(
        height=550, xaxis_title="Total Readmissions",
        yaxis_title="Medical Specialty", margin=dict(l=20, r=70, t=60, b=40),
    )
    st.plotly_chart(fig_specialty, use_container_width=True)


elif page == "🧠 Readmission Prediction":
    st.title("🧠 Hospital Readmission Prediction")

    st.write(
        "Predict the probability of hospital readmission "
        "within 30 days using Machine Learning."
    )

    st.divider()

    model_path = (
        Path(__file__).resolve().parent.parent
        / "models"
        / "random_forest_model.pkl"
    )

    if model_path.exists():
        try:
            model = joblib.load(model_path)
            st.success("Random Forest Model Loaded Successfully!")
            st.info("Model is ready. Patient input form will be added next.")

            st.subheader("👤 Enter Patient Details")

            with st.form("prediction_form"):
                col1, col2 = st.columns(2)

                with col1:
                    age = st.selectbox(
                        "Age Group",
                        ["[0-10)", "[10-20)", "[20-30)", "[30-40)",
                         "[40-50)", "[50-60)", "[60-70)",
                         "[70-80)", "[80-90)", "[90-100)"]
                    )

                    gender = st.selectbox(
                        "Gender", ["Female", "Male", "Unknown/Invalid"]
                    )

                    race = st.selectbox(
                        "Race",
                        ["Caucasian", "AfricanAmerican", "Asian",
                         "Hispanic", "Other", "Unknown"]
                    )

                    admission_type_id = st.selectbox(
                        "Admission Type",
                        [1, 2, 3, 4, 5, 6, 7, 8],
                        format_func=lambda x: {
                            1: "Emergency",
                            2: "Urgent",
                            3: "Elective",
                            4: "Newborn",
                            5: "Not Available",
                            6: "Unknown",
                            7: "Trauma Center",
                            8: "Not Mapped"
                        }.get(x, str(x))
                    )

                    time_in_hospital = st.number_input(
                        "Hospital Stay (Days)", 1, 14, 4
                    )

                    num_lab_procedures = st.number_input(
                        "Number of Lab Procedures", 0, 150, 40
                    )

                    num_procedures = st.number_input(
                        "Number of Procedures", 0, 20, 1
                    )

                with col2:
                    num_medications = st.number_input(
                        "Number of Medications", 0, 100, 15
                    )

                    number_outpatient = st.number_input(
                        "Previous Outpatient Visits", 0, 100, 0
                    )

                    number_emergency = st.number_input(
                        "Previous Emergency Visits", 0, 100, 0
                    )

                    number_inpatient = st.number_input(
                        "Previous Inpatient Visits", 0, 100, 0
                    )

                    number_diagnoses = st.number_input(
                        "Number of Diagnoses", 1, 20, 7
                    )

                    A1Cresult = st.selectbox(
                        "A1C Test Result",
                        ["None", "Norm", ">7", ">8"]
                    )

                    diabetesMed = st.selectbox(
                        "Diabetes Medication",
                        ["Yes", "No"]
                    )

                
                predict_button = st.form_submit_button(
                    "🔍 Predict Readmission Risk",
                    use_container_width=True
                )

            if predict_button:
                patient_data = pd.DataFrame([{
                    "race": race,
                    "gender": gender,
                    "age": age,
                    "admission_type_id": admission_type_id,
                    "time_in_hospital": time_in_hospital,
                    "num_lab_procedures": num_lab_procedures,
                    "num_procedures": num_procedures,
                    "num_medications": num_medications,
                    "number_outpatient": number_outpatient,
                    "number_emergency": number_emergency,
                    "number_inpatient": number_inpatient,
                    "number_diagnoses": number_diagnoses,
                    "A1Cresult": A1Cresult,
                    "diabetesMed": diabetesMed
                }])

                
                probability = float(
                    model.predict_proba(patient_data)[0][1]
                )

                st.divider()
                st.subheader("📊 Patient Readmission Risk Assessment")

                if probability < 0.30:
                    risk_level = "LOW"
                    risk_message = (
                        "The model indicates a comparatively "
                        "lower estimated readmission risk."
                    )
                elif probability < 0.60:
                    risk_level = "MODERATE"
                    risk_message = (
                        "The model indicates an intermediate "
                        "estimated readmission risk."
                    )
                else:
                    risk_level = "HIGH"
                    risk_message = (
                        "The model indicates a comparatively "
                        "higher estimated readmission risk."
                    )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Model Risk Score",
                        f"{probability * 100:.2f}%"
                    )

                with col2:
                    st.metric(
                        "Risk Category (Demo)",
                        risk_level
                    )

                st.progress(probability)

                if risk_level == "LOW":
                    st.success(
                        "🟢 Low Risk Category"
                    )
                elif risk_level == "MODERATE":
                    st.warning(
                        "🟡 Moderate Risk Category"
                    )
                else:
                    st.error(
                        "🔴 High Risk Category"
                    )

                st.write("### 📋 Prediction Interpretation")
                st.write(risk_message)

                st.info(
                    "This result is generated by an experimental "
                    "Random Forest model trained on historical "
                    "hospital data."
                )

                st.caption(
                    "Disclaimer: The risk categories use illustrative "
                    "thresholds of 30% and 60%. The model score is not "
                    "a calibrated clinical probability. This system is "
                    "for educational and research demonstration only, "
                    "not for medical decisions."
                )

        except Exception as e:
            st.error(f"Error loading model: {e}")
    else:
        st.error("Model file not found!")


elif page == "📈 Model Evaluation":
    st.title("📈 Machine Learning Model Evaluation")

    st.write(
        "Performance comparison of Logistic Regression "
        "and Random Forest for 30-day hospital readmission prediction."
    )

    results = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC AUC"
        ],
        "Logistic Regression": [
            67.41, 17.03, 49.63, 25.36, 64.19
        ],
        "Random Forest": [
            68.34, 17.54, 49.67, 25.93, 64.55
        ]
    })

    st.subheader("📊 Model Performance Comparison")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    chart_data = results.melt(
        id_vars="Metric",
        var_name="Model",
        value_name="Score"
    )

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Score",
        color="Model",
        barmode="group",
        text="Score",
        title="Logistic Regression vs Random Forest",
        color_discrete_map={
            "Logistic Regression": "#7856B8",
            "Random Forest": "#008C95"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Score (%)",
        yaxis_range=[0, 100],
        xaxis_title="Evaluation Metric"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Model Comparison Summary")

    st.success(
        "Random Forest achieved slightly better scores "
        "across all five reported evaluation metrics."
    )

    st.write(
        "**Random Forest Accuracy:** 68.34%"
    )

    st.write(
        "**Random Forest F1 Score:** 25.93%"
    )

    st.write(
        "**Random Forest ROC AUC:** 64.55%"
    )

    st.warning(
        "The models have limited predictive performance, "
        "particularly low precision. Results are from an "
        "initial encounter-level train-test split. "
        "Patient-level validation and probability calibration "
        "are needed before interpreting predictions as clinical risk."
    )

elif page == "ℹ️ About Project":
    st.title("ℹ️ About the Project")
    st.write(
        "This project analyzes hospital readmissions using Python, MySQL, "
        "Machine Learning, and Power BI."
    )
    st.subheader("Technologies Used")
    st.write("Python | Pandas | MySQL | Scikit-learn | Power BI | Streamlit")
