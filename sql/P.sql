
CREATE DATABASE IF NOT EXISTS hospital_dw;

USE hospital_dw;

SELECT DATABASE();


USE hospital_dw;

-- Dimension 1: Patient information
CREATE TABLE IF NOT EXISTS Dim_Patient (
    patient_key INT AUTO_INCREMENT PRIMARY KEY,
    patient_nbr BIGINT NOT NULL UNIQUE,
    race VARCHAR(50),
    gender VARCHAR(20),
    age_group VARCHAR(20)
);

-- Dimension 2: Diagnosis
CREATE TABLE IF NOT EXISTS Dim_Diagnosis (
    diagnosis_key INT AUTO_INCREMENT PRIMARY KEY,
    diag_1 VARCHAR(20),
    diag_2 VARCHAR(20),
    diag_3 VARCHAR(20),
    diagnosis_category VARCHAR(100)
);

-- Dimension 3: Admission type
CREATE TABLE IF NOT EXISTS Dim_Admission_Type (
    admission_type_key INT AUTO_INCREMENT PRIMARY KEY,
    admission_type_id INT NOT NULL UNIQUE,
    admission_type_name VARCHAR(100)
);

-- Dimension 4: Discharge
CREATE TABLE IF NOT EXISTS Dim_Discharge (
    discharge_key INT AUTO_INCREMENT PRIMARY KEY,
    discharge_disposition_id INT NOT NULL UNIQUE,
    discharge_description VARCHAR(150)
);

-- Dimension 5: Admission source
CREATE TABLE IF NOT EXISTS Dim_Admission_Source (
    admission_source_key INT AUTO_INCREMENT PRIMARY KEY,
    admission_source_id INT NOT NULL UNIQUE,
    admission_source_name VARCHAR(150)
);

-- Dimension 6: Payer
CREATE TABLE IF NOT EXISTS Dim_Payer (
    payer_key INT AUTO_INCREMENT PRIMARY KEY,
    payer_code VARCHAR(20) NOT NULL UNIQUE
);

-- Dimension 7: Medical specialty
CREATE TABLE IF NOT EXISTS Dim_Specialty (
    specialty_key INT AUTO_INCREMENT PRIMARY KEY,
    medical_specialty VARCHAR(100) NOT NULL UNIQUE
);

-- Fact table: One row per hospital encounter
CREATE TABLE IF NOT EXISTS Fact_Admission (
    encounter_id BIGINT PRIMARY KEY,
    patient_key INT,
    diagnosis_key INT,
    admission_type_key INT,
    discharge_key INT,
    admission_source_key INT,
    payer_key INT,
    specialty_key INT,
    time_in_hospital INT,
    num_lab_procedures INT,
    num_procedures INT,
    num_medications INT,
    number_outpatient INT,
    number_emergency INT,
    number_inpatient INT,
    readmitted_30d TINYINT,
    FOREIGN KEY (patient_key)
        REFERENCES Dim_Patient(patient_key),
    FOREIGN KEY (diagnosis_key)
        REFERENCES Dim_Diagnosis(diagnosis_key),
    FOREIGN KEY (admission_type_key)
        REFERENCES Dim_Admission_Type(admission_type_key),
    FOREIGN KEY (discharge_key)
        REFERENCES Dim_Discharge(discharge_key),
    FOREIGN KEY (admission_source_key)
        REFERENCES Dim_Admission_Source(admission_source_key),
    FOREIGN KEY (payer_key)
        REFERENCES Dim_Payer(payer_key),
    FOREIGN KEY (specialty_key)
        REFERENCES Dim_Specialty(specialty_key)
);

SHOW TABLES;

