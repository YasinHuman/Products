from flask import Blueprint, g, request
from .methods import *
import json
from .validators import *

login_bp = Blueprint("login", __name__)

ACCOUNTS_PATH = "data/accounts.json"

try:
    with open(ACCOUNTS_PATH, 'r') as file:
        accounts = json.load(file)
except(json.JSONDecodeError):
    accounts = []

@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()

    error, userId = validateLoginData(data=data, accounts=accounts)
    if error:
        return error

    token, expiration = generateToken(userId=userId, accounts=accounts)
    return saveToken(userId=userId, token=token, expiration=expiration, accounts=accounts)