def checkCategoryParams(data, isPut):
    if type(data) != dict:
        return "Data should be a dictionary", 400

    if not isPut:   
        if set(data) != set(["title", "description"]):
            return {"error": "Submit Title and Description and no more"}, 400

        if data["title"] == "":
            return {"error": "A title is needed"}, 400

        if data["description"] == "":
            return {"error": "A description is needed"}, 400

    if isPut:
        if not all(data_ in ["id", "title", "description"] for data_ in data):
            return {"error": "Wrong keys"}, 400

    return None


def checkProductsForDelete(categoryId, products):
    for product in products:
         if product["categoryId"] == categoryId and not product["is_deleted"]:
              return {"error": "Cannot delete category with existing products"}, 400
    return None