def validateLoginData(accounts, data):
    if not data:
        return ({"error": "Missing JSON data"}, 400), None

    for account in accounts:
        if account["username"] == data["username"] and account["password"] == data["password"] and not account["is_deleted"]:
            return None, account["id"]
    return ({"error": "Invalid username or password"}, 401), None