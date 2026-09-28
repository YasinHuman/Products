from flask import Blueprint, current_app, request
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