from flask import Blueprint

show = Blueprint('show',__name__)

from main.showBook import views
