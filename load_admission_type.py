import pandas as pd
import mysql.connector
import getpass

mapping_path = r"C:\Hospital_Readmission_Project\data\IDS_mapping.csv"
csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"

df = pd.read_csv(csv_path, low_memory=False)

# Mapping file contains multiple sections
with open(mapping_path, "r", encoding="utf-8-sig") as file:
    lines = file.readlines()

start = next(
    i for i, line in enumerate(lines)
    if line.strip().lower() == "admission_type_id,description"
)

mapping_rows = []

for line in lines[start + 1:]:
    line = line.strip()

    if not line:
        break

    parts = line.split(",", 1)

    if len(parts) == 2:
        admission_id = parts[0].strip()
        description = parts[1].strip()

        if admission_id.isdigit():
            mapping_rows.append(
                (int(admission_id), description)
            )
        else:
            break

mapping = dict(mapping_rows)
admission_ids = sorted(
    df["admission_type_id"].dropna().astype(int).unique()
)

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
INSERT INTO Dim_Admission_Type
(admission_type_id, admission_type_name)
VALUES (%s, %s)
ON DUPLICATE KEY UPDATE
admission_type_name = VALUES(admission_type_name)
"""

data = [
    (int(admission_id),
     mapping.get(int(admission_id), "Unknown"))
    for admission_id in admission_ids
]

cursor.executemany(insert_query, data)
connection.commit()

print("Admission Type dimension loaded successfully!")

cursor.execute("""
    SELECT admission_type_id, admission_type_name
    FROM Dim_Admission_Type
    ORDER BY admission_type_id
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()