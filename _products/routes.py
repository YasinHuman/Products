from flask import Blueprint, request
from .methods import *
from .validators import *
from ..validators import *

products_bp = Blueprint("products", __name__)


@products_bp.route('/', methods=["POST"])
def createProduct():
    data = request.get_json(silent=True)

    error = checkProductParams(data=data, isPutOrRead=False)
    error = checkForCategory(data=data)
    error = checkForImage(data=data)
    
    if error:
        return error

    return saveProductData(data=data)
   
@products_bp.route('/', methods=["GET"])
def readProduct(): 
    productFilters = request.get_json(silent=True)
    error = checkProductParams(data=productFilters, isPutOrRead=True)

    if error:
        return error

    return productFilter(filters=productFilters)


@products_bp.route('/', methods=["PUT"])
def updateProduct():
    data = request.get_json(silent=True)

    error = checkProductParams(data=data, isPutOrRead=True)
    error = checkForCategory(data=data)
    error = checkForImage(data=data)
    if error:
        return error

    return updateProductData(data=data)


@products_bp.route('/', methods=["DELETE"])
def deleteProduct():
    data = request.get_json(silent=True)

    error = checkDeleteParams(data=data)
    if error:
        return error

    return deleteProductData(data=data)


@products_bp.route('/<int:id>')
def getProductById(id):
    return productFilter(filters={"id":id})