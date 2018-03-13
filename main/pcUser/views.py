from flask import render_template
from main.pcUser import pcUser

@pcUser.route('/pcUser')
def showUser():
    return render_template('pcUser.html')

