import pandas as pd

csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"

df = pd.read_csv(csv_path, low_memory=False)

print("CSV loaded successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nTarget column:")
print(df["readmitted_30d"].value_counts())

print("\nTotal missing values:")
print(df.isnull().sum().sum())

import mysql.connector
import getpass

password = getpass.getpass("Enter MySQL password (blank if none): ")

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=password,
    database="hospital_dw"
)

cursor = connection.cursor()

print("\nConnected to MySQL successfully!")

patient_df = df[
    ["patient_nbr", "race", "gender", "age"]
].drop_duplicates(subset=["patient_nbr"])

patient_df = patient_df.rename(
    columns={"age": "age_group"}
)

insert_query = """
INSERT INTO Dim_Patient
(patient_nbr, race, gender, age_group)
VALUES (%s, %s, %s, %s)
"""

patient_data = list(
    patient_df.itertuples(index=False, name=None)
)

cursor.executemany(insert_query, patient_data)

connection.commit()

print("Patient dimension loaded successfully!")
print("Total unique patients:", len(patient_data))

cursor.execute("SELECT COUNT(*) FROM Dim_Patient")
print("Rows in Dim_Patient:", cursor.fetchone()[0])

cursor.close()
connection.close()