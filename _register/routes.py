from flask import Blueprint, request
from .methods import *
from .validators import *

register_bp = Blueprint("register", __name__)

@register_bp.route('/', methods=["POST"])
def registerAccount():
    data = request.get_json()

    error = checkRegisterParams(data=data)
    if error:
        return error

    return saveAccount(data=data)