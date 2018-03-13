from flask import Blueprint, request, render_template, make_response,url_for,redirect
from main.dbCon.dbForUser import dbForUser

from main.forUser import user

@user.route('/user/register', methods =['POST'])
def registerUser():
    user = userInfo(request.form['userName'],request.form['password'],'FT')    
    conn = dbForUser()
    num = conn.insertUser(user.userName,user.password,user.userType)
    if num > 0:
        resp = make_response(redirect(url_for('index.home',msg = '4')))

        resp.set_cookie('userName',request.form['userName'])
        resp.set_cookie('userType','FT')
        
        return resp

    else:
        return redirect(url_for('index.home',msg = '5'))


@user.route('/user/login', methods =['POST'])
def LoginUser():
    userName = request.form['userName']
    password = request.form['password']
    conn = dbForUser()
    result = conn.userLogin(userName,password)
    if result.userName != '':
        resp = make_response(redirect(url_for('index.home',msg = '6')))

        resp.set_cookie('userName',userName)
        resp.set_cookie('userType',result.userType)
        
        return resp
    else:
        return redirect(url_for('index.home',msg = '7'))


@user.route('/user/loginOut')
def loginOut():
    resp = make_response(redirect(url_for('index.home')))
    resp.set_cookie('userName','',expires=0)
    resp.set_cookie('userType','',expires=0)

    return resp

class userInfo(object):
    def __init__(self, userName,password,userType):
        self.userName = userName
        self.password = password
        self.userType = userType