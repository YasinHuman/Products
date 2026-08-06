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
    error = None
    
    error = checkCategoryParams(data, False)
    if error:
        return error

    categories = saveCategoryData(data=data, categories=categories, CATEGORIES_PATH=CATEGORIES_PATH) # Saves data and updates it for later use

    return {"Result": "Data received",
            "Categories":[{k: v for k, v in category.items() if k != "is_deleted"} for category in categories if not category.get("is_deleted", False)]}, 200
   

@categories_bp.route('/', methods=["GET"])
def readCategory():
    categoryFilters = request.get_json(silent=True)
    
    if type(categoryFilters) != dict:
            return {"error": "Filters should be a dictionary"}, 400

    return categoryFilter(filters=categoryFilters, categories=categories)


@categories_bp.route('/', methods=["PUT"])
def updateCategory():
    global categories
    data = request.get_json(silent=True)
    error = None

    error = checkCategoryParams(data=data, isPut=True)
    if error:
        return error

    return updateCategoryData(data=data, categories=categories, CATEGORIES_PATH=CATEGORIES_PATH)
    

@categories_bp.route('/', methods=["DELETE"])
def deleteCategory():
    global categories
    data = request.get_json(silent=True)

    if type(data) != dict or "id" not in data:
        return "Category ID is required for deletion", 400

    return deleteCategoryData(data=data, categories=categories, products=products, CATEGORIES_PATH=CATEGORIES_PATH)

