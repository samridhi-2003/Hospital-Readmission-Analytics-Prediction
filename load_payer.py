import pandas as pd
import mysql.connector
import getpass

csv_path = r"C:\Hospital_Readmission_Project\data\hospital_cleaned.csv"

df = pd.read_csv(csv_path, low_memory=False)

payer_codes = (
    df["payer_code"]
    .fillna("Unknown")
    .astype(str)
    .drop_duplicates()
    .tolist()
)

print("Unique payer codes:", len(payer_codes))

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
INSERT INTO Dim_Payer (payer_code)
VALUES (%s)
ON DUPLICATE KEY UPDATE
payer_code = VALUES(payer_code)
"""

payer_data = [(code,) for code in payer_codes]

cursor.executemany(insert_query, payer_data)

connection.commit()

print("\nPayer dimension loaded successfully!")

cursor.execute("SELECT COUNT(*) FROM Dim_Payer")

print("Rows in Dim_Payer:", cursor.fetchone()[0])

cursor.execute("""
SELECT payer_key, payer_code
FROM Dim_Payer
ORDER BY payer_key
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()