import mysql.connector
from mysql.connector import Error
connection = None

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='epic_events',
        user='epic_user',
        password='epic@123'
    )

    if connection.is_connected():
        print("Connected to MySQL database")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print(f"Using database: {db[0]}")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
