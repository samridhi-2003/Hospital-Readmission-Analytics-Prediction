import pandas as pd
import mysql.connector
import getpass
import csv

csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"
mapping_path = r"C:\Hospital_Readmission_Project\data\IDS_mapping.csv"

df = pd.read_csv(csv_path, low_memory=False)

mapping = {}
reading_section = False

with open(mapping_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)

    for row in reader:
        if not row:
            continue

        first = row[0].strip()

        if first.lower() == "admission_source_id":
            reading_section = True
            continue

        if reading_section:
            if first.isdigit():
                description = ",".join(row[1:]).strip()
                mapping[int(first)] = description
            elif first:
                break

admission_source_ids = sorted(
    df["admission_source_id"]
    .dropna()
    .astype(int)
    .unique()
)

print("Mapping entries found:", len(mapping))

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
INSERT INTO Dim_Admission_Source
(admission_source_id, admission_source_name)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE
admission_source_name = VALUES(admission_source_name)
"""

data = [
    (
        int(source_id),
        mapping.get(int(source_id), "Unknown")
    )
    for source_id in admission_source_ids
]

cursor.executemany(insert_query, data)
connection.commit()

print("\nAdmission Source dimension loaded successfully!")

cursor.execute("""
SELECT admission_source_id, admission_source_name
FROM Dim_Admission_Source
ORDER BY admission_source_id
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()