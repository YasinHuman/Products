import mysql.connector as mysql
from flask import g

def saveAccount(data):
    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "INSERT INTO accounts (username, fullName, password) VALUES (%s, %s, %s)"
    values = (data["username"], data["full name"], data["password"])
    cursor.execute(query, values)
    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Success": "account created successfully"}, 201
        