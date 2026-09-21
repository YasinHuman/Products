import json
from .validators import checkProductsForDelete

def categoryFilter(filters, categories, products):
    filterResults = []
    if not all(filter_ in ["title", "description", "id"] for filter_ in filters):
                return {"error": "Wrong filter keys"}, 400
    
    for category in categories:
        if category["is_deleted"]:
            continue

        if "title" in filters and filters["title"].lower() not in category["title"].lower():
            continue

        if "description" in filters and filters["description"].lower() not in category["description"].lower():
            continue

        if "id" in filters and int(filters["id"]) != int(category["id"]):
            continue

        childProducts = []
        for product in products:
            if int(product.get("categoryId")) == category.get('id') and not product.get("is_deleted"):
                childProducts.append({k: v for k, v in product.items() if k not in ["is_deleted", "categoryId"]})
        category["products"] = childProducts

        filterResults.append(category)        
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200

def saveCategoryData(data, categories, CATEGORIES_PATH):
    categoryId = 1
    if categories:
        categoryId = len(categories)+1
    data = {
        "id":categoryId,
        **data,
        "is_deleted":False
    }

    categories.append(data)
    with open(CATEGORIES_PATH, 'w') as file:
        json.dump(categories, file, indent=3)

    return categories

def updateCategoryData(data, categories, CATEGORIES_PATH):
    categoryId = data.get("id")

    for category in categories:
        if category["id"] == categoryId and not category["is_deleted"]:
            for key, value in data.items():
                if key in ["title", "description"]:
                    category[key] = value
            with open(CATEGORIES_PATH, 'w') as file:
                json.dump(categories, file, indent=3)
            return {"Result": "Category updated",
                    "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200

    return {"error": "Category not found"}, 404

def deleteCategoryData(data, products, categories, CATEGORIES_PATH):
    categoryId = data["id"]
    error = None

    error = checkProductsForDelete(categoryId, products)
    if error:
        return error

    for category in categories:
        if category["id"] == categoryId and not category["is_deleted"]:
            category["is_deleted"] = True
            with open(CATEGORIES_PATH, 'w') as file:
                json.dump(categories, file, indent=3)
            return {"Result": "Category deleted",
                    "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200

    return {"error": "Category not found"}, 404