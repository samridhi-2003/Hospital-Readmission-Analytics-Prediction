import mysql.connector
import getpass

password = getpass.getpass("Enter MySQL password (blank if none): ")

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=password,
        database="hospital_dw"
    )

    print("MySQL connected successfully!")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")

    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)