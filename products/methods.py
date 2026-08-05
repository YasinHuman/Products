def productFilter(filters, products):
    filterResults = []
    if not all(filter_ in ["title", "description", "id", "price", "categoryId"] for filter_ in filters):
                return "Wrong filter keys", 400
    for product in products:
        matches = True

        if str(filters["title"]).lower() not in str(product["title"]).lower():
            matches = False
            break

        if str(filters["description"]).lower() not in str(product["description"]).lower():
            matches = False
            break

        if str(filters["id"]).lower() not in str(product["id"]).lower():
            matches = False
            break

        if str(filters["price"]).lower() not in str(product["price"]).lower():
            matches = False
            break

        if str(filters["categoryId"]).lower() not in str(product["categoryId"]).lower():
            matches = False
            break

        if matches and not product["is_deleted"]:
            filterResults.append(product)
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200
