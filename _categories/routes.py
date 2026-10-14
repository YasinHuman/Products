from flask import Blueprint, request
from .methods import *
from .validators import *
import json
from ..validators import *
import mysql.connector as mysql

categories_bp = Blueprint("categories", __name__)

@categories_bp.route('/', methods=["POST"])
def createCategory():
    data = request.get_json(silent=True)
    
    error = checkCategoryParams(data=data, isPutOrRead=False)
    if error:
        return error

    return saveCategoryData(data=data)

@categories_bp.route('/', methods=["GET"])
def readCategory():
    categoryFilters = request.get_json(silent=True)

    error = checkCategoryParams(categoryFilters, isPutOrRead=True)
    if error:
        return error

    return categoryFilter(filters=categoryFilters)


@categories_bp.route('/', methods=["PUT"])
def updateCategory():
    global categories
    data = request.get_json(silent=True)

    error = checkCategoryParams(data=data, isPutOrRead=True)
    error = checkForImage(data=data)
    if error:
        return error

    return updateCategoryData(data=data)
    

@categories_bp.route('/', methods=["DELETE"])
def deleteCategory():
    global categories
    data = request.get_json(silent=True)

    error = checkDeleteParams(data=data)
    error = checkProductsForDelete(data=data, categoryOrImage="category")
    if error:
        return error

    return deleteCategoryData(data=data)


@categories_bp.route('/<int:id>')
def getCategoryById(id):
    return categoryFilter(filters={"id":id})