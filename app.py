from flask import Flask, request, g
from _categories.routes import categories_bp
from _products.routes import products_bp
from _uploads.routes import uploads_bp
from _login.routes import login_bp
from _register.routes import register_bp
from datetime import datetime
import mysql.connector as mysql

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  


@app.before_request
def checkUser():
    g.databaseConfig = {
    'host': 'localhost',
    'user': 'root',
    'password': "!E12DB3b00h@",
    'database': 'ecommerce'
}
    if request.endpoint in ["login", "register"]:
        return

    token = request.headers.get("x-token")

    cnx = mysql.connect(**g.get('databaseConfig'))
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT id, token, tokenExpiration, isAdmin FROM accounts")
    accounts = cursor.fetchall()

    for account in accounts:
        if account.get("token") == token:
            expiration = account.get("tokenExpiration")

            if expiration:
                tokenExpiration = datetime.fromisoformat(expiration)

                if datetime.now() < tokenExpiration:
                    g.isAdmin = account.get("isAdmin", False)
                    g.userId = account.get("id")
                    
                    cursor.close()
                    cnx.close()
                    return

    cursor.close()
    cnx.close()
    return {"error": "Unauthorized"}, 401



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