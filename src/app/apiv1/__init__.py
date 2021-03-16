from flask import Blueprint

api = Blueprint('apiv1', __name__)

# This modules need to be imported after the above api is defined, because the "api" variable is imported in each file
from . import testapp