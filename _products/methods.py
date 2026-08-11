import json

def productFilter(filters, products, categories):
    filterResults = []  
    if not all(filter_ in ["title", "description", "id", "price", "categoryId", "imageId"] for filter_ in filters):
                return "Wrong filter keys", 400
    
    for product in products:
        if product["is_deleted"]:
            continue
        
        if "title" in filters and filters["title"].lower() not in product["title"].lower():
            continue

        if "description" in filters and filters["description"].lower() not in product["description"].lower():
            continue

        if "id" in filters and int(filters["id"]) != int(product["id"]):
            continue    

        if "price" in filters and float(filters["price"]) != float(product["price"]):
            continue

        if "categoryId" in filters and int(filters["categoryId"]) != int(product["categoryId"]):
            continue

        if "imageId" in filters and int(filters["imageId"]) != int(product["imageId"]):
            continue

        categoryName = categories[int(product.get("categoryId"))-1].get("title")
        product["categoryName"] = categoryName
        
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