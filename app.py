from flask import Flask
from categories.routes import categories_bp
from products.routes import products_bp
from uploads.routes import uploads_bp

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  

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