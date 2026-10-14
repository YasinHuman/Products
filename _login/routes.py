from flask import Blueprint, g, request
from .methods import *
from .validators import *

login_bp = Blueprint("login", __name__)


@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()

    error, userId = validateLoginData(data=data)
    if error:
        return error

    token, expiration = generateToken(userId=userId)
    return saveToken(userId=userId, token=token, expiration=expiration)