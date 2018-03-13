from flask import Blueprint

user = Blueprint('user',__name__)

from main.forUser import views
