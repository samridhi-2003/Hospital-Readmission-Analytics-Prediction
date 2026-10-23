USE hospital_dw;

SELECT 'Dim_Patient' AS table_name, COUNT(*) AS total_rows
FROM Dim_Patient

UNION ALL

SELECT 'Dim_Diagnosis', COUNT(*)
FROM Dim_Diagnosis

UNION ALL

SELECT 'Dim_Admission_Type', COUNT(*)
FROM Dim_Admission_Type

UNION ALL

SELECT 'Dim_Discharge', COUNT(*)
FROM Dim_Discharge

UNION ALL

SELECT 'Dim_Admission_Source', COUNT(*)
FROM Dim_Admission_Source

UNION ALL

SELECT 'Dim_Payer', COUNT(*)
FROM Dim_Payer

UNION ALL

SELECT 'Dim_Specialty', COUNT(*)
FROM Dim_Specialty

UNION ALL

SELECT 'Fact_Admission', COUNT(*)
FROM Fact_Admission;