import pandas as pd
import mysql.connector
import getpass

df = pd.read_csv(
    r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv",
    low_memory=False
)

diagnosis_df = df[
    ["diag_1", "diag_2", "diag_3"]
].drop_duplicates().copy()

diagnosis_df = diagnosis_df.fillna("Unknown")

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

cursor.execute("SELECT COUNT(*) FROM Dim_Diagnosis")
existing_rows = cursor.fetchone()[0]

if existing_rows == 0:

    insert_query = """
    INSERT INTO Dim_Diagnosis
    (diag_1, diag_2, diag_3, diagnosis_category)
    VALUES (%s, %s, %s, %s)
    """

    diagnosis_data = [
        (row.diag_1, row.diag_2, row.diag_3, None)
        for row in diagnosis_df.itertuples(index=False)
    ]

    cursor.executemany(insert_query, diagnosis_data)
    connection.commit()

    print("Diagnosis dimension loaded successfully!")
else:
    print("Dim_Diagnosis already contains data. Skipping insert.")

cursor.execute("SELECT COUNT(*) FROM Dim_Diagnosis")

print("Unique diagnosis combinations:", len(diagnosis_df))
print("Rows in Dim_Diagnosis:", cursor.fetchone()[0])

cursor.close()
connection.close()