"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask,request, g, send_from_directory,render_template
import os 
from main.showIndex import index
from main.showImage import onRoad
from main.showBook import show 
from main.bookImageEdit import bookImageEdit
from main.adminEdit import adminEdit
from main.forUser import user 
from main.pcUser import pcUser
app = Flask(__name__ ,template_folder =os.path.abspath('.')+ '\\templates',static_folder=os.path.abspath('.') + '\\static')

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.before_request
def login_before_request():
    userName = request.cookies.get('userName',None)
    userType = request.cookies.get('userType',None)
    if userName is not None:
        from main.dbCon.dbForUser import dbForUser
        conn = dbForUser()
        user = conn.findUser(userName)
    else:
        user = None
    g.user = user
    g.type = userType

#注册蓝本
app.register_blueprint(index)
app.register_blueprint(onRoad)
app.register_blueprint(show)
app.register_blueprint(bookImageEdit)
app.register_blueprint(adminEdit)
app.register_blueprint(user)
app.register_blueprint(pcUser)


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def error_500(e):
    from main.dbCon.dbErrorLog import dbErrorLog
    db = dbErrorLog()
    db.errorLog(e.args[0],'500')
    return render_template('500.html'),500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
