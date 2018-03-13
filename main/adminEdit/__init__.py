from flask import Blueprint

adminEdit = Blueprint('adminEdit',__name__)

from main.adminEdit import views
