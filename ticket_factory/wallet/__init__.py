from .bus_pass import Pass
from flask import Blueprint

pass_builder = Pass()

api = Blueprint('api', __name__)
