def checkCategoryParams(data, isPut):
    if type(data) != dict:
        return "Data should be a dictionary", 400

    if not isPut:   
        if set(data) != set(["title", "description"]):
            return "Submit Title and Description and no more", 400

    if data["title"] == "":
         return "A title is needed", 400

    if data["description"] == "":
         return "A description is needed", 400

    if isPut:
        if data["id"] == "":
            return "An id is needed", 400
        if set(data) != set(["id", "title", "description"]):
                    return "Submit Id, Title and Description and no more", 400

    return "Valid"


def checkProductsForDelete(categoryId, products):
    for product in products:
         if product["categoryId"] == categoryId and not product["is_deleted"]:
              return "Invalid"
    return "Valid"