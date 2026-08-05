from flask import Blueprint, request
from .methods import *
from .validators import *
import json

categories_bp = Blueprint("categories", __name__)

CATEGORIES_PATH = 'data/categories.json'
PRODUCTS_PATH = 'data/products.json'

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

@categories_bp.route('/', methods=["POST"])
def createCategory():
    global categories
    data = request.get_json(silent=True)

    if checkCategoryParams(data, False) != "Valid":
        return checkCategoryParams(data, False)

    createCategory(categories, CATEGORIES_PATH)

    return {"Result": "Data received",
            "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200
   

@categories_bp.route('/', methods=["GET"])
def readCategory():
    categoryFilters = request.get_json(silent=True)
    
    if not categoryFilters:
        return [{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)], 200

    if type(categoryFilters) != dict:
            return "Filters should be a dictionary", 400

    return categoryFilter(categoryFilters, categories)


@categories_bp.route('/', methods=["PUT"])
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
    

@categories_bp.route('/', methods=["DELETE"])
def deleteCategory():
    global categories
    data = request.get_json(silent=True)

    if type(data) != dict or "id" not in data:
        return "Category ID is required for deletion", 400

    categoryId = data["id"]
    
    if checkProductsForDelete(categoryId, products) != "Valid":
        return "Products are assigned to this category. Either change their category or delete them to delete this category.", 400
    
    for category in categories:
        if category["id"] == categoryId and not category["is_deleted"]:
            category["is_deleted"] = True
            with open(CATEGORIES_PATH, 'w') as file:
                json.dump(categories, file, indent=3)
            return {"Result": "Category deleted",
                    "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200

    return "Category not found", 404
