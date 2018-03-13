from flask import Blueprint

bookImageEdit = Blueprint('bookImageEdit',__name__)

from main.bookImageEdit import views
