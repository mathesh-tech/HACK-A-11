from flask import Blueprint

query_bp = Blueprint('query_bp', __name__)
dashboard_bp = Blueprint('dashboard_bp', __name__)

from . import query
from . import dashboard
