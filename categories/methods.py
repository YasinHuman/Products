import json
def categoryFilter(filters, categories):
    filterResults = []
    if not all(filter_ in ["title", "description", "id"] for filter_ in filters):
                return "Wrong filter keys", 400
    for category in categories:
        matches = True

        if str(filters["title"]).lower() not in str(category["title"]).lower():
            matches = False
            break

        if str(filters["description"]).lower() not in str(category["description"]).lower():
            matches = False
            break

        if str(filters["id"]).lower() not in str(category["id"]).lower():
            matches = False
            break

        if matches and not category["is_deleted"]:
            filterResults.append(category)
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200

def createCategory(categories, CATEGORIES_PATH):
    categoryId = 1
    if categories:
        categoryId = len(categories)+1
    data = {
        "id":categoryId,
        **data,
        "is_deleted":False
    }

    categories.append(data)
    with open(CATEGORIES_PATH, 'w') as file:
        json.dump(categories, file, indent=3)
    