import pandas as pd
import mysql.connector
import getpass

csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"

df = pd.read_csv(csv_path, low_memory=False)

specialties = (
    df["medical_specialty"]
    .fillna("Unknown")
    .astype(str)
    .drop_duplicates()
    .tolist()
)

print("Unique medical specialties:", len(specialties))

password = getpass.getpass(
    "Enter MySQL password (blank if none): "
)

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=password,
    database="hospital_dw"
)

cursor = connection.cursor()

insert_query = """
INSERT INTO Dim_Specialty (medical_specialty)
VALUES (%s)
ON DUPLICATE KEY UPDATE
medical_specialty = VALUES(medical_specialty)
"""

specialty_data = [(specialty,) for specialty in specialties]

cursor.executemany(insert_query, specialty_data)

connection.commit()

print("\nSpecialty dimension loaded successfully!")

cursor.execute("SELECT COUNT(*) FROM Dim_Specialty")

print("Rows in Dim_Specialty:", cursor.fetchone()[0])

cursor.execute("""
SELECT specialty_key, medical_specialty
FROM Dim_Specialty
ORDER BY specialty_key
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()