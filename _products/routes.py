from flask import Blueprint, request
from .methods import *
import json
from .validators import *

products_bp = Blueprint("products", __name__)

PRODUCTS_PATH = 'data/products.json'
CATEGORIES_PATH = 'data/categories.json'
UPLOADS_DATA_PATH = 'data/uploads.json'

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
try:
    with open(UPLOADS_DATA_PATH, 'r') as file:
        uploadsData = json.load(file)
except(json.JSONDecodeError):
    uploadsData = []

@products_bp.route('/', methods=["POST"])
def createProduct():
    global products
    data = request.get_json(silent=True)
    error = None

    error = checkProductParams(data=data, isPut=False)
    if error:
        return error

    error = checkForCategory(categories=categories, data=data)
    if error:
        return error

    error = checkForImage(uploads=uploadsData, data=data)
    if error:
        return error

    products = saveProductData(data=data, products=products, PRODUCTS_PATH=PRODUCTS_PATH) # Saves data but also updates it for later use

    return {"Result": "Data received",
            "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200

   
@products_bp.route('/', methods=["GET"])
def readProduct():
    productFilters = request.get_json(silent=True)
    
    if type(productFilters) != dict:
            return "Filters should be a dictionary", 400

    return productFilter(filters=productFilters, products=products, categories=categories)


@products_bp.route('/', methods=["PUT"])
def updateProduct():
    global products
    data = request.get_json(silent=True)
    error = None

    error = checkProductParams(data=data, isPut=True)
    if error:
        return error

    return updateProductData(products=products, data=data, PRODUCTS_PATH=PRODUCTS_PATH)


@products_bp.route('/', methods=["DELETE"])
def deleteProduct():
    global products
    data = request.get_json(silent=True)

    if type(data) != dict or "id" not in data:
        return "Product ID is required for deletion, and it must be submitted in a json file", 400

    return deleteProductData(data=data,products=products,PRODUCTS_PATH=PRODUCTS_PATH)


@products_bp.route('/<int:id>')
def getProductById(id):
    return productFilter(filters={"id":id}, products=products, categories=categories)