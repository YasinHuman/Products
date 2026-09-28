from flask import Flask, json, request
from _categories.routes import categories_bp
from _products.routes import products_bp
from _uploads.routes import uploads_bp

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  
ACCOUNTS_PATH = 'data/accounts.json'

try:
    with open(ACCOUNTS_PATH, 'r') as file:
        accounts = json.load(file)
except(json.JSONDecodeError):
    accounts = []

try:
    with open('data/adminsIds.json', 'r') as file:
        admins_ids = json.load(file)
except(json.JSONDecodeError):
    admins_ids = []


@app.before_request
def check_header():
    username = request.headers.get("X-user-username")
    if not username:
        return json.jsonify({"error": "Missing X-user-username header"}), 400
    password = request.headers.get("X-user-password")
    if not password:
        return json.jsonify({"error": "Missing X-user-password header"}), 400

    for account in accounts:
        if not account["username"] == username and not account["password"] == password:
            return json.jsonify({"error": "Invalid username or password"}), 401
        if account["username"] == username and account["password"] == password:
            userId = account["id"]

    app.config['userId'] = userId

    if userId in admins_ids:
        app.config['is_admin'] = True
    else:
        app.config['is_admin'] = False

app.register_blueprint(
    categories_bp,
    url_prefix="/categories"
)

app.register_blueprint(
    products_bp,
    url_prefix="/products"
)

app.register_blueprint(
    uploads_bp,
    url_prefix="/uploads"
)

if __name__ == '__main__':
    app.run(debug=True, port=5000)