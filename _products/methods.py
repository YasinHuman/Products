from flask import g
import mysql.connector as mysql
from datetime import datetime

def productFilter(filters):
    isAdmin = g.get('isAdmin')
    userId = g.get('userId')
    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    usedFilters = []
    values = []

    for key, value in filters.items():
        usedFilters.append(f"{key} = %s")
        values.append(value)

    query = "SELECT * FROM products WHERE isDeleted = 0"
    if usedFilters:
        query += " AND " + " AND ".join(usedFilters)
    if not isAdmin:
        query += " AND createdBy = %s"
        values.append(userId)
    cursor.execute(query, values)

    dummy = cursor.fetchall()

    result = []
    for row in dummy:
        product = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "price": row[3],
            "categoryId": row[4],
            "imageId": row[5],
            "createdBy": row[7],
            "createdAt": row[8].isoformat(),
            "updatedAt": row[9].isoformat() if row[9] else None
        }
        result.append(product)
    cursor.close()
    cnx.close()
    
    return result


def saveProductData(data):
    userId = g.get('userId')

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = """INSERT INTO products (title, description, price, categoryId, imageId, isDeleted, createdBy, createdAt, updatedAt)
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = [data["title"], data["description"], data["price"], data["categoryId"], data["imageId"], False, userId, datetime.now(), None]
    cursor.execute(query, values)

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Result": "Data received"}, 200
    
    

def updateProductData(data):
    productId = data.get("id")
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "SELECT createdBy FROM products WHERE id = %s AND isDeleted = 0"
    cursor.execute(query, [productId])
    result = cursor.fetchone()
    
    if not result or (not isAdmin and result[0] != userId):
        cursor.close()
        cnx.close()
        return {"error": "Product not found"}, 404

    updateFields = ["updatedAt = %s"]
    values = [datetime.now()]

    for key in data:
        updateFields.append(f"{key} = %s")
        values.append(data[key])

    query = "UPDATE products SET " + ", ".join(updateFields) + " WHERE id = %s"
    cursor.execute(query, values + [productId])

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Result": "Data updated"}, 200


def deleteProductData(data):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')
    productId = data["id"]

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "SELECT createdBy, isDeleted FROM products WHERE id = %s AND isDeleted = 0"
    cursor.execute(query, [productId])
    result = cursor.fetchone()

    if not result or (not isAdmin and result[0] != userId) or result[1]:
        cursor.close()
        cnx.close()
        return {"error": "Product not found"}, 404

    query = "UPDATE products SET isDeleted = 1 WHERE id = %s"
    cursor.execute(query, [productId])

    cnx.commit()
    cursor.close()
    cnx.close()