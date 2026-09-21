from flask import Flask, json, request
from _categories.routes import categories_bp
from _products.routes import products_bp
from _uploads.routes import uploads_bp

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  
ACCOUNTS_PATH = 'data/accounts.json'

try:
    with open(ACCOUNTS_PATH, 'r') as file:
        account = json.load(file)
except(json.JSONDecodeError):
    accounts = []


@app.before_request
def check_header():
    id = request.headers.get("X-user-id")

    ids = [account.get("id") for account in accounts if not account.get("is_deleted", False)]
    if id not in ids:
        return {"error": "Invalid API key"}, 400

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