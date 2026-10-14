import mysql.connector as mysql
from flask import g

def validateLoginData(data):
    if not data:
        return ({"error": "Missing JSON data"}, 400), None

    cnx =  mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT username, password, id, is_deleted FROM accounts")
    accounts = cursor.fetchall()

    for account in accounts:
        if account["username"] == data["username"] and account["password"] == data["password"] and not account["is_deleted"]:
            return None, account["id"]
    return ({"error": "Invalid username or password"}, 401), None