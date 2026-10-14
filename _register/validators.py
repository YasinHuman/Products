import mysql.connector as mysql
from flask import g

def checkRegisterParams(data):
    if set(data) != {"username","full name","password","password confirmation"}:
        return {"error": "Your full name, username, password, and password confirmation are required"}, 400

    if data["password"] != data["password confirmation"]:
        return {"error": "Password doesn't match confirmation password"}, 400

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()
    query = "SELECT username FROM accounts WHERE username = %s"
    cursor.execute(query, (data["username"],))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result:
        return {"error": "Username taken"}, 400

    return None