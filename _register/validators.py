def checkRegisterParams(data, accounts):
    if set(data) != {"username","full name","password","password confirmation"}:
        return {"error": "Your full name, username, password, and password confirmation are required"}, 400

    if data["password"] != data["password confirmation"]:
        return {"error": "Password doesn't match confirmation password"}, 400

    for account in accounts:
        if data["username"] == account["username"]:
            return {"error": "Username taken"}, 400

    return None