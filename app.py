from flask import Flask, json, request, g
from _categories.routes import categories_bp
from _products.routes import products_bp
from _uploads.routes import uploads_bp
from _login.routes import login_bp
from _register.routes import register_bp

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  
ACCOUNTS_PATH = 'data/accounts.json'

try:
    with open(ACCOUNTS_PATH, 'r') as file:
        accounts = json.load(file)
except(json.JSONDecodeError):
    accounts = []


### CHANGE LATER
@app.before_request
def check_user():
    g.is_admin = True
    g.userId = 1001
###


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

app.register_blueprint(
    login_bp,
    url_prefix="/login"
)

app.register_blueprint(
    register_bp,
    url_prefix="/register"
)

if __name__ == '__main__':
    app.run(debug=True, port=5000)