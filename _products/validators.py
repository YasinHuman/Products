def checkProductParams(data, isPut):
    if type(data) != dict:
        return "Data should be a dictionary", 400
    
    if not isPut:
        if set(data) != set(["title", "description", "price", "categoryId", "imageId"]):
            return {"error": "Submit Title, Description, Price and Category Id, Image Id and no more"}, 400

        if data["title"] == "":
            return {"error": "A title is needed"}, 400

        if data["description"] == "":
            return {"error": "A description is needed"}, 400

        if data["price"] == "":
            return {"error": "A price is needed"}, 400

        if data["categoryId"] == "":
            return {"error": "A category Id is needed"}, 400

        if data["imageId"] == "":
                return {"error": "An image Id is needed"}, 400

        return None

    if isPut:
        if not all(data_ in ["title", "description", "id", "price", "categoryId", "imageId"] for data_ in data):
                        return "Wrong keys", 400
        

def checkForCategory(categories, data):
    for category in categories:
        if str(data["categoryId"]) == str(category["id"]):
            return None
    return {"error": "Category doesn't exist"}, 400

def checkForImage(data, uploads):
    for upload in uploads:
        if str(data["imageId"]) == str(upload["id"]):
            return None
    return {"error": "Image doesn't exist"}, 400
