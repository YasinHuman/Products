import json

def productFilter(filters, products):
    filterResults = []
    if not filters:
        return [{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)], 200
    
    if not all(filter_ in ["title", "description", "id", "price", "categoryId", "imageId"] for filter_ in filters):
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

        if str(filters["imageId"]).lower() not in str(product["imageId"]).lower():
                matches = False
                break

        if matches and not product["is_deleted"]:
            filterResults.append(product)
    return [{k: v for k, v in filterResult.items() if k != "is_deleted"} for filterResult in filterResults], 200

def saveProductData(data, products, PRODUCTS_PATH):
    productId = 1
    if products:
        productId = len(products)+1
    data = {
        "id":productId,
        **data,
        "is_deleted":False
    }
    products.append(data)
    with open(PRODUCTS_PATH, 'w') as file:
        json.dump(products, file, indent=3)

    return products


def updateProductData(products, data, PRODUCTS_PATH):
    productId = data.get("id")
    for product in products:
            if product["id"] == productId and not product["is_deleted"]:
                for key, value in data.items():
                    product[key] = value
                with open(PRODUCTS_PATH, 'w') as file:
                    json.dump(products, file, indent=3)
                return {"Result": "Product updated",
                        "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200
    return {"error": "Product not found"}, 404


def deleteProductData(data, products, PRODUCTS_PATH):
    productId = data["id"]
    for product in products:
        if product["id"] == productId and not product["is_deleted"]:
            product["is_deleted"] = True
            with open(PRODUCTS_PATH, 'w') as file:
                json.dump(products, file, indent=3)
            return {"Result": "Product deleted",
                    "Products":[{k: v for k, v in product.items() if k != "is_deleted"} for product in products if not product.get("is_deleted", False)]}, 200

    return {"error": "Product not found"}, 404