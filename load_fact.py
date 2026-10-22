import pandas as pd
import mysql.connector
import getpass

csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"

df = pd.read_csv(csv_path, low_memory=False)

password = getpass.getpass("Enter MySQL password (blank if none): ")

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=password,
    database="hospital_dw"
)

cursor = connection.cursor(dictionary=True)

def read_table(query):
    cursor.execute(query)
    return pd.DataFrame(cursor.fetchall())

patient = read_table(
    "SELECT patient_key, patient_nbr FROM Dim_Patient"
)

diagnosis = read_table(
    "SELECT diagnosis_key, diag_1, diag_2, diag_3 FROM Dim_Diagnosis"
)

admission = read_table(
    "SELECT admission_type_key, admission_type_id FROM Dim_Admission_Type"
)

discharge = read_table(
    "SELECT discharge_key, discharge_disposition_id FROM Dim_Discharge"
)

source = read_table(
    "SELECT admission_source_key, admission_source_id FROM Dim_Admission_Source"
)

payer = read_table(
    "SELECT payer_key, payer_code FROM Dim_Payer"
)

specialty = read_table(
    "SELECT specialty_key, medical_specialty FROM Dim_Specialty"
)

df = df.merge(patient, on="patient_nbr", how="left")

df = df.merge(
    diagnosis,
    on=["diag_1", "diag_2", "diag_3"],
    how="left"
)

df = df.merge(admission, on="admission_type_id", how="left")

df = df.merge(
    discharge,
    on="discharge_disposition_id",
    how="left"
)

df = df.merge(source, on="admission_source_id", how="left")
df = df.merge(payer, on="payer_code", how="left")
df = df.merge(specialty, on="medical_specialty", how="left")

key_columns = [
    "patient_key",
    "diagnosis_key",
    "admission_type_key",
    "discharge_key",
    "admission_source_key",
    "payer_key",
    "specialty_key"
]

print("\nUnmatched dimension keys:")
print(df[key_columns].isnull().sum())

if df[key_columns].isnull().any().any():
    cursor.close()
    connection.close()
    raise ValueError("Some dimension keys are missing. Fact loading stopped.")

if len(df) != 101766:
    cursor.close()
    connection.close()
    raise ValueError("Unexpected number of rows after merging.")

columns = [
    "encounter_id",
    "patient_key",
    "diagnosis_key",
    "admission_type_key",
    "discharge_key",
    "admission_source_key",
    "payer_key",
    "specialty_key",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "readmitted_30d"
]

insert_query = """
INSERT INTO Fact_Admission (
    encounter_id, patient_key, diagnosis_key,
    admission_type_key, discharge_key,
    admission_source_key, payer_key, specialty_key,
    time_in_hospital, num_lab_procedures,
    num_procedures, num_medications,
    number_outpatient, number_emergency,
    number_inpatient, readmitted_30d
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

cursor.execute("SELECT COUNT(*) AS total FROM Fact_Admission")
existing = cursor.fetchone()["total"]

if existing > 0:
    print("Fact_Admission already has", existing, "rows.")
    print("Skipping insert to avoid duplicate records.")
else:
    print("\nStarting fact table loading...")

    batch_size = 2000

    for start in range(0, len(df), batch_size):
        batch = df.iloc[start:start + batch_size][columns]

        records = [
            tuple(int(value) for value in row)
            for row in batch.itertuples(index=False, name=None)
        ]

        cursor.executemany(insert_query, records)
        connection.commit()

        print("Inserted:", min(start + batch_size, len(df)))

    print("\nFact table loading completed!")

cursor.execute("SELECT COUNT(*) AS total FROM Fact_Admission")
print("Total fact rows:", cursor.fetchone()["total"])

cursor.close()
connection.close()