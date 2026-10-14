from datetime import datetime
import os
from uuid import *
from flask import g
import mysql.connector as mysql

UPLOADS_IMAGE_PATH = "images"

def assignAndSaveData(filename):
    userId = g.get('userId')
    extension = str(filename).rsplit(".", maxsplit=1)[1].lower()
    codeName = uuid4().hex

    cnx = mysql.connect(**g.get("databaseConfig"))
    cursor = cnx.cursor(dictionary=True)

    query = """INSERT INTO images (originalName, codeName, isDeleted, createdBy, createdAt)
    values (%s, %s, %s, %s, %s)"""

    values = [filename, codeName+"."+extension, False, userId, datetime.now()]
    cursor.execute(query, values)
    cnx.commit()
    cursor.close()
    cnx.close()
    return codeName+"."+extension

def saveFile(codename, file):
    path = os.path.join(UPLOADS_IMAGE_PATH, codename)
    file.save(path)
    return {"Result": "File has been uploaded"}, 200

def changeData(data):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    cnx = mysql.connect(**g.get("databaseConfig"))
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT id, createdBy FROM images where id = %s"
    cursor.execute(query, [data["id"]])
    result = cursor.fetchone()

    if not result or (userId != result["createdBy"] and not isAdmin):
        cursor.close()
        cnx.close()
        return {"error": "Image not found"}, 404

    query = "UPDATE images SET originalName = %s, updatedAt = %s WHERE id = %s"
    values = [data["filename"], datetime.now(), data["id"]]
    cursor.execute(query, values)
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"Result": "Image updated"}, 200


def deleteFile(data):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    cnx = mysql.connect(**g.get("databaseConfig"))
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT id, createdBy FROM images where id = %s"
    cursor.execute(query, [data["id"]])
    result = cursor.fetchone()

    if not result or (userId != result["createdBy"] and not isAdmin):
        cursor.close()
        cnx.close()
        return {"error": "Image not found"}, 404

    query = "UPDATE images SET isDeleted = 1, updatedAt = %s WHERE id = %s"
    cursor.execute(query, [datetime.now(), data["id"]])
    cnx.commit()
    cursor.close()
    cnx.close()
    return {"Result": "Image deleted"}, 200