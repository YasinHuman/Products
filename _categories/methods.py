from datetime import datetime
import json
from .validators import checkProductsForDelete
from flask import g
import mysql.connector as mysql


def categoryFilter(filters):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')
    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    usedFilters = []
    values = []
    
    for key, value in filters.items():
        usedFilters.append(f"{key} = %s")
        values.append(value)

    query = "SELECT * FROM categories WHERE isDeleted = 0"
    if usedFilters:
        query += " AND " + " AND ".join(usedFilters)
    if not isAdmin:
        query += " AND createdBy = %s"
        values.append(userId)
    cursor.execute(query, values)

    dummy = cursor.fetchall()

    result = []
    for row in dummy:
        category = {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "imageId": row[3],
            "isDeleted": row[4],
            "createdBy": row[5],
            "createdAt": row[6].isoformat(),
            "updatedAt": row[7].isoformat() if row[7] else None
        }
        result.append(category)
    cursor.close()
    cnx.close()
    


def saveCategoryData(data):
    userId = g.get('userId')

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = """INSERT INTO categories (title, description, imageId, isDeleted, createdBy, createdAt, updatedAt)
    values (%s, %s, %s, %s, %s, %s, %s)"""

    values = [data["title"], data["description"], data["imageId"], False, userId, datetime.now(), None]
    cursor.execute(query, values)

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Result": "Data saved"}, 201

def updateCategoryData(data):
    categoryId = data.get("id")
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "SELECT createdBy FROM categories WHERE id = %s AND isDeleted = 0"
    cursor.execute(query, [categoryId])
    result = cursor.fetchone()

    if not result or (not isAdmin and result[0] != userId):
        cursor.close()
        cnx.close()
        return {"error": "Category not found"}, 404

    updateFields = ["updatedAt = %s"]
    values = [datetime.now()]

    for key in data:
        updateFields.append(f"{key} = %s")
        values.append(data[key])

    query = "UPDATE categories SET " + ", ".join(updateFields) + " WHERE id = %s"
    cursor.execute(query, values + [categoryId])

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Result": "Data updated"}, 200

def deleteCategoryData(data):
    categoryId = data.get("id")
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "SELECT createdBy FROM categories WHERE id = %s AND isDeleted = 0"
    cursor.execute(query, [categoryId])
    result = cursor.fetchone()

    if not result or (not isAdmin and result[0] != userId):
        cursor.close()
        cnx.close()
        return {"error": "Category not found"}, 404

    query = "SELECT id, categoryId, isDeleted FROM products WHERE categoryId = %s"
    cursor.execute(query, [categoryId])
    products = cursor.fetchall()

    error = checkProductsForDelete(categoryId, products)
    if error:
        cursor.close()
        cnx.close()
        return error

    query = "UPDATE categories SET isDeleted = 1, updatedAt = %s WHERE id = %s"
    cursor.execute(query, [datetime.now(), categoryId])

    cnx.commit()
    cursor.close()
    cnx.close()

    return {"Result": "Category deleted"}, 200
