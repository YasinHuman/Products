from flask import Blueprint, request
from .methods import *
import json
from .validators import *

uploads_bp = Blueprint("uploads", __name__)

UPLOADS_IMAGE_PATH = "images"
UPLOADS_DATA_PATH = "data/uploads.json"
try:
    with open(UPLOADS_DATA_PATH, 'r') as file:
        uploadsData = json.load(file)
except(FileNotFoundError, json.JSONDecodeError):
    uploadsData = []

@uploads_bp.route('/', methods=["POST"])
def createUpload():
    global uploadsData
    file = request.files.get("file")
    error = None
    
    error = checkFile(file, file.filename)
    if error:
        return error
    
    data = assignData(file.filename, uploadsData)
    
    error = saveFile(data=data, file=file, uploads=uploadsData)
    if error:
        return error
    
    
    return "File has been saved"

@uploads_bp.route('/', methods=["GET"])
def readUpload():
    pass

@uploads_bp.route('/', methods=["PUT"])
def updateUpload():
    global uploadsData
    file = request.files.get("file")
    data = request.get_json()["changes"]
    error = None

    error = checkFile(file, file.filename)
    if error:
        return error

    changeData(data=data, uploads=uploadsData)

    return "Data changed", 200
    


@uploads_bp.route('/', methods=["DELETE"])
def deleteUpload():
    global uploadsData
    data = request.get_json()["changes"]
    deleteFile(data=data, uploads=uploadsData)

    return "File has been deleted", 200
