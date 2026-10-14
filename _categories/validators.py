def checkCategoryParams(data, isPutOrRead):
    if type(data) != dict:
        return "Data should be a dictionary", 400

    if not isPutOrRead:   
        if set(data) != set(["title", "description", "imageId"]):
            return {"error": "Submit Title and Description and no more"}, 400

    if isPutOrRead:
        if not all(data_ in ["id", "title", "description", "imageId", "products"] for data_ in data):
            return {"error": "Wrong keys"}, 400

    if data["title"].strip() == "" or isPutOrRead and "title" in data and data["title"].strip() == "":
            return {"error": "A title is needed"}, 400
        
    if data["description"].strip() == "" or isPutOrRead and "description" in data and data["description"].strip() == "":
        return {"error": "A description is needed"}, 400
    
    return None
