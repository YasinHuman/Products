import os
from uuid import *
import json
from flask import g

UPLOADS_IMAGE_PATH = "images"
UPLOADS_DATA_PATH = "data/uploads.json"

def assignData(filename, uploads):
    userId = g.get('userId')
    fileId = max((upload["id"] for upload in uploads), default=0) + 1
    extension = str(filename).rsplit(".", maxsplit=1)[1].lower()
    codeName = uuid4().hex
    
    data = {
        "id": fileId,
        "originalName":filename,
        "codeName":f"{codeName}.{extension}",
        "is_deleted": False,
        "created_by": userId
        }
    return data

def saveFile(data, file, uploads):
    path = os.path.join(UPLOADS_IMAGE_PATH, data["codeName"])
    file.save(path)

    uploads.append(data)
    with open(UPLOADS_DATA_PATH, 'w') as file_:
        json.dump(uploads, file_, indent=3)
    return None


def changeData(data, uploads):
    userId = g.get('userId')
    is_admin = g.get('is_admin')
    for upload in uploads:
        if data["id"] == upload["id"]:
            if not is_admin and upload.get("created_by") != userId:
                return {"error": "Permission denied"}, 403
            upload["originalName"] = data["filename"]
    with open(UPLOADS_DATA_PATH, 'w') as file:
        json.dump(uploads, file, indent=3)


def deleteFile(data, uploads):
    userId = g.get('userId')
    is_admin = g.get('is_admin')
    for upload in uploads:
        if data["id"] == upload["id"]:
            if not is_admin and upload.get("created_by") != userId:
                return {"error": "Permission denied"}, 403
            upload["is_deleted"] = True
    with open(UPLOADS_DATA_PATH, 'w') as file:
        json.dump(uploads, file, indent=3)