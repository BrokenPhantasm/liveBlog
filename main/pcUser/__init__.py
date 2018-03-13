from flask import Blueprint

pcUser = Blueprint('pcUser',__name__)

from main.pcUser import views
