import os
from uuid import *
import json

def assignData(filename, uploads):
    fileId = max((upload["id"] for upload in uploads), default=0) + 1
    extension = str(filename).rsplit(".", maxsplit=1)[1].lower()
    codeName = uuid4().hex
    
    data = {
        "id": fileId,
        "originalName":filename,
        "codeName":f"{codeName}.{extension}",
        "is_deleted": False
        }
    return data

def saveFile(data, dataFolder, uploadFolder, file, uploads):
    path = os.path.join(uploadFolder, data["codeName"])
    file.save(path)

    uploads.append(data)
    with open(dataFolder, 'w') as file_:
        json.dump(uploads, file_, indent=3)
    return None


def changeData(data, uploads, dataPath):
    for upload in uploads:
        if data["id"] == upload["id"]:
            upload["originalName"] = data["filename"]
    with open(dataPath, 'w') as file:
        json.dump(uploads, file, indent=3)


def deleteFile(data, uploads, dataPath, uploadFolder):
    for upload in uploads:
        if data["id"] == upload["id"]:
            upload["is_deleted"] = True
            # path = os.path.join(uploadFolder, upload["codeName"])
            # if os.path.exists(path):
            #     os.remove(path)
    with open(dataPath, 'w') as file:
        json.dump(uploads, file, indent=3)