from flask import Blueprint, current_app, request
from .methods import *
import json
from .validators import *

register_bp = Blueprint("register", __name__)

ACCOUNTS_PATH = "data/accounts.json"

try:
    with open(ACCOUNTS_PATH, 'r') as file:
        accounts = json.load(file)
except(json.JSONDecodeError):
    accounts = []

@register_bp.route('/', methods=["POST"])
def registerAccount():
    data = request.get_json()

    error = checkRegisterParams(data=data, accounts=accounts)
    if error:
        return error

    return saveAccount(data=data, accounts=accounts)