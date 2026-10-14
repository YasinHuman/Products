from flask import Blueprint, request
from ..validators import *
from .methods import *
import json
from .validators import *

uploads_bp = Blueprint("uploads", __name__)

@uploads_bp.route('/', methods=["POST"])
def createUpload():
    file = request.files.get("file")
    
    error = checkFile(file, file.filename)
    if error:
        return error
    
    codename = assignAndSaveData(file.filename)
    
    return saveFile(codename=codename, file=file)

@uploads_bp.route('/', methods=["GET"])
def readUpload():
    pass

@uploads_bp.route('/', methods=["PUT"])
def updateUpload():
    data = request.get_json(silent=True)
    
    error = checkFile(file=None, filename=data.get("filename"), isPutOrRead=True)
    if error:
        return error

    return changeData(data=data)
    


@uploads_bp.route('/', methods=["DELETE"])
def deleteUpload():
    data = request.get_json()

    error = checkDeleteParams(data=data)
    error = checkProductsForDelete(data=data, categoryOrImage="image")
    if error:
        return error

    return deleteFile(data=data)
