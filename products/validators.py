def checkProductParams(data, isPut):
    if type(data) != dict:
        return "Data should be a dictionary", 400

    if not isPut:   
        if set(data) != set(["title", "description", "price", "categoryId"]):
            return "Submit Title, Description, Price and Category Id and no more", 400

    if data["title"] == "":
         return "A title is needed", 400

    if data["description"] == "":
         return "A description is needed", 400

    if data["price"] == "":
         return "A price is needed", 400

    if data["categoryId"] == "":
         return "A categoryId is needed", 400

    if isPut:
        if data["id"] == "":
            return "An id is needed", 400
        if set(data) != set(["id", "title", "description", "price", "categoryId"]):
                    return "Submit Id, Title, Description, Price and Category Id and no more", 400

    return "Valid"

def checkForCategory(categories, data):
    for category in categories:
        if str(data["categoryId"]) == str(category["categoryId"]):
             return "Valid"
        return "Invalid"

