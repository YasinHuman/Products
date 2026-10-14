from flask import g
import mysql.connector as mysql


def checkProductParams(data, isPutOrRead):
    if type(data) != dict:
        return "Data should be a dictionary", 400
    
    if not isPutOrRead:
        if set(data) != set(["title", "description", "price", "categoryId", "imageId"]):
            return {"error": "Submit Title, Description, Price and Category Id, Image Id and no more"}, 400

    if isPutOrRead:
        if not all(data_ in ["title", "description", "id", "price", "categoryId", "imageId"] for data_ in data):
                        return "Wrong keys", 400

    if data["title"].strip() == "" or isPutOrRead and "title" in data and data["title"].strip() == "":
        return {"error": "A title is needed"}, 400
    
    if data["description"].strip() == "" or isPutOrRead and "description" in data and data["description"].strip() == "":
        return {"error": "A description is needed"}, 400

    if (data["price"].strip() == "" or float(data["price"].strip()) <= 0) or isPutOrRead and "price" in data and (data["price"].strip() == "" or float(data["price"].strip()) <= 0):
        return {"error": "A valid price is needed"}, 400

    return None
        

def checkForCategory(data):
    userId = g.get('userId')
    isAdmin = g.get('isAdmin')
    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor()

    query = "SELECT id, createdBy FROM categories WHERE id = %s"
    cursor.execute(query, [data["categoryId"]])
    result = cursor.fetchone()

    if not result or (userId != result[1] and not isAdmin):
         cursor.close()
         cnx.close()
         return {"error": "Category not found"}

    cursor.close()
    cnx.close()

    return None
    

    
