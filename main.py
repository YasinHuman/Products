from flask import *
import json
from methods import *

app = Flask(__name__)

# CATEGORIES

CATEGORIES_PATH = '.\data\categories.json'

try:
    with open(CATEGORIES_PATH, 'r') as file:
        categories = json.load(file)
except(json.JSONDecodeError):
    categories = []

@app.route('/categories', methods=["POST"])
def createCategory():
    global categories
    data = request.get_json(silent=True)

    if checkCategoryParams(data, False) != "Valid":
        return checkCategoryParams(data, False)

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

    return {"Result": "Data received",
            "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200
   

@app.route('/categories', methods=["GET"])
def readCategory():
    categoryFilters = request.get_json(silent=True)
    
    if not categoryFilters:
        return [{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)], 200

    if type(categoryFilters) != dict:
            return "Filters should be a dictionary", 400

    return categoryFilter(categoryFilters, categories)

@app.route('/categories', methods=["PUT"])
def updateCategory():
    global categories
    data = request.get_json(silent=True)

    if checkCategoryParams(data, True) != "Valid":
        return checkCategoryParams(data, True)

    categoryId = data.get("id")

    for category in categories:
        if category["id"] == categoryId and not category["is_deleted"]:
            category.update({
                "title": data["title"],
                "description": data["description"]
            })
            with open(CATEGORIES_PATH, 'w') as file:
                json.dump(categories, file, indent=3)
            return {"Result": "Category updated",
                    "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200

    return "Category not found", 404
    

@app.route('/categories', methods=["DELETE"])
def deleteCategory():
    global categories
    data = request.get_json(silent=True)

    if type(data) != dict or "id" not in data:
        return "Category ID is required for deletion", 400

    categoryId = data["id"]
    for category in categories:
        if category["id"] == categoryId and not category["is_deleted"]:
            category["is_deleted"] = True
            with open(CATEGORIES_PATH, 'w') as file:
                json.dump(categories, file, indent=3)
            return {"Result": "Category deleted",
                    "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200

    return "Category not found", 404


# PRODUCTS

PRODUCTS_PATH = '.\data\products.json'

try:
    with open(PRODUCTS_PATH, 'r') as file:
        products = json.load(file)
except(json.JSONDecodeError):
    products = []

@app.route('/products', methods=["POST"])
def createProduct():
    global products
    data = request.get_json(silent=True)

    if checkProductParams(data, False) != "Valid":
        return checkProductParams(data, False)

    productId = 1
    if products:
        productId = len(products)+1
    data = {
        "id":productId,
        **data,
        "is_deleted":False
    }

    products.append(data)
    with open(PRODUCTS_PATH, 'w') as file:
        json.dump(products, file, indent=3)

    return {"Result": "Data received",
            "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200
   
@app.route('/products', methods=["GET"])
def readProduct():
    productFilters = request.get_json(silent=True)
    
    if not productFilters:
        return [{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)], 200

    if type(productFilters) != dict:
            return "Filters should be a dictionary", 400

    return productFilter(productFilters, products)

@app.route('products', methods=["PUT"])
def updateProduct():
    global products
    data = request.get_json(silent=True)

    if checkProductParams(data, True) != "Valid":
        return checkProductParams(data, True)

    productId = data.get("id")

    for product in products:
        if product["id"] == productId and not product["is_deleted"]:
            product.update({
                "title": data["title"],
                "description": data["description"],
                "price": data["price"],
                "category_id": data["category_id"]
            })
            with open(PRODUCTS_PATH, 'w') as file:
                json.dump(products, file, indent=3)
            return {"Result": "Product updated",
                    "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200

    return "Product not found", 404

@app.route('products', methods=["DELETE"])
def deleteProduct():
    global products
    data = request.get_json(silent=True)

    if type(data) != dict or "id" not in data:
        return "Product ID is required for deletion", 400

    productId = data["id"]
    for product in products:
        if product["id"] == productId and not product["is_deleted"]:
            product["is_deleted"] = True
            with open(PRODUCTS_PATH, 'w') as file:
                json.dump(products, file, indent=3)
            return {"Result": "Product deleted",
                    "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200

    return "Product not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=9000)