from flask import Blueprint, request
from .methods import *
import json
from .validators import *

products_bp = Blueprint("products", __name__)

PRODUCTS_PATH = 'data/products.json'
CATEGORIES_PATH = 'data/categories.json'

try:
    with open(CATEGORIES_PATH, 'r') as file:
        categories = json.load(file)
except(json.JSONDecodeError):
    categories = []
try:
    with open(PRODUCTS_PATH, 'r') as file:
        products = json.load(file)
except(json.JSONDecodeError):
    products = []

@products_bp.route('/', methods=["POST"])
def createProduct():
    global products
    data = request.get_json(silent=True)

    if checkProductParams(data, False) != "Valid":
        return checkProductParams(data, False)

    if checkForCategory(categories, data) != "Valid":
        return "Category doesn't exist", 400

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

   
@products_bp.route('/', methods=["GET"])
def readProduct():
    productFilters = request.get_json(silent=True)
    
    if not productFilters:
        return [{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)], 200

    if type(productFilters) != dict:
            return "Filters should be a dictionary", 400

    return productFilter(productFilters, products)


@products_bp.route('/', methods=["PUT"])
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


@products_bp.route('/', methods=["DELETE"])
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