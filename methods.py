import json

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

def categoryFilter(filters, categories):
    filterResults = []
    if not all(filter_ in ["title", "description", "id"] for filter_ in filters):
                return "Wrong filter keys", 400
    for category in categories:
        matches = True

        if str(filters["title"]).lower() not in str(category["title"]).lower():
            matches = False
            break

        if str(filters["description"]).lower() not in str(category["description"]).lower():
            matches = False
            break

        if str(filters["id"]).lower() not in str(category["id"]).lower():
            matches = False
            break

        if matches and not category["is_deleted"]:
            filterResults.append(category)
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200


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

    if data["quantity"] == "":
         return "A quantity is needed", 400

    if isPut:
        if data["id"] == "":
            return "An id is needed", 400
        if set(data) != set(["id", "title", "description", "price", "categoryId"]):
                    return "Submit Id, Title, Description, Price and Category Id and no more", 400

    return "Valid"

def productFilter(filters, products):
    filterResults = []
    if not all(filter_ in ["title", "description", "id", "price", "categoryId"] for filter_ in filters):
                return "Wrong filter keys", 400
    for product in products:
        matches = True

        if str(filters["title"]).lower() not in str(product["title"]).lower():
            matches = False
            break

        if str(filters["description"]).lower() not in str(product["description"]).lower():
            matches = False
            break

        if str(filters["id"]).lower() not in str(product["id"]).lower():
            matches = False
            break

        if str(filters["price"]).lower() not in str(product["price"]).lower():
            matches = False
            break

        if str(filters["categoryId"]).lower() not in str(product["categoryId"]).lower():
            matches = False
            break

        if matches and not product["is_deleted"]:
            filterResults.append(product)
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200

