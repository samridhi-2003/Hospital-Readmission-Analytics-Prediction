USE hospital_dw;

SELECT
    COUNT(*) AS total_admissions,
    COUNT(DISTINCT patient_key) AS total_patients,
    SUM(readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission;

USE hospital_dw;

SELECT
    p.age_group,
    COUNT(*) AS total_admissions,
    SUM(f.readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(f.readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission f
JOIN Dim_Patient p
    ON f.patient_key = p.patient_key
GROUP BY p.age_group
ORDER BY readmission_rate DESC;

USE hospital_dw;

SELECT
    a.admission_type_name,
    COUNT(*) AS total_admissions,
    SUM(f.readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(f.readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission f
JOIN Dim_Admission_Type a
    ON f.admission_type_key = a.admission_type_key
GROUP BY a.admission_type_name
ORDER BY readmission_rate DESC;


USE hospital_dw;

SELECT
    s.medical_specialty,
    COUNT(*) AS total_admissions,
    SUM(f.readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(f.readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission f
JOIN Dim_Specialty s
    ON f.specialty_key = s.specialty_key
GROUP BY s.medical_specialty
HAVING COUNT(*) >= 100
ORDER BY readmission_rate DESC;

USE hospital_dw;

SELECT
    time_in_hospital AS hospital_stay_days,
    COUNT(*) AS total_admissions,
    SUM(readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission
GROUP BY time_in_hospital
ORDER BY time_in_hospital ASC;

USE hospital_dw;

SELECT
    d.diag_1 AS primary_diagnosis,
    COUNT(*) AS total_admissions,
    SUM(f.readmitted_30d) AS total_readmissions,
    ROUND(
        100.0 * SUM(f.readmitted_30d) / COUNT(*),
        2
    ) AS readmission_rate
FROM Fact_Admission f
JOIN Dim_Diagnosis d
    ON f.diagnosis_key = d.diagnosis_key
GROUP BY d.diag_1
HAVING COUNT(*) >= 100
ORDER BY readmission_rate DESC;

