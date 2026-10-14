import mysql.connector as mysql
from flask import g

def checkForImage(data):
    cnx = mysql.connect(**g.get("databaseConfig"))
    cursor = cnx.cursor()
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    query = "SELECT id, createdBy FROM images where id = %s"
    cursor.execute(query, [data["imageId"]])
    result = cursor.fetchone()

    if not result or (userId != result[1] and not isAdmin):
        cursor.close()
        cnx.close()
        return {"error": "Image not found"}

    return None

def checkProductsForDelete(data, categoryOrImage):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    if categoryOrImage == "category":
        cnx = mysql.connect(**g.get("databaseConfig"))
        cursor = cnx.cursor()
        query = "SELECT id FROM products where categoryId = %s"
        cursor.execute(query, [data["id"]])
        products = cursor.fetchall()
        cursor.close()
        cnx.close()

    if categoryOrImage == "image":
        cnx = mysql.connect(**g.get("databaseConfig"))
        cursor = cnx.cursor()
        query = "SELECT id FROM products where imageId = %s"
        cursor.execute(query, [data["id"]])
        products = cursor.fetchall()
        cursor.close()
        cnx.close()

    if products:
        return {"error": f"Cannot delete {categoryOrImage}. There are products associated with it."}


def checkDeleteParams(data):
    if type(data) != dict:
        return {"error": "Data format should be json"}, 400

    if "id" not in data:
        return {"error": "Product ID is required for deletion"}, 400

    return None