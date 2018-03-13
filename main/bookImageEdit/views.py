# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request , redirect, url_for,send_from_directory
import re
from main.dbCon.dbBookImageEdit import dbBookImageEdit
from main.pubCore.userVerification import admin_request
from main.bookImageEdit import bookImageEdit

from werkzeug import secure_filename
from PIL import Image 
from main.dbCon.dbErrorLog import dbErrorLog
import urllib.parse
from datetime import datetime
import random
import config
import os

@bookImageEdit.route('/bookImageEdit')
@admin_request
def default():
    return render_template(
        'BookImageEdit.html',
        title = '流年暗渡'
        )

@bookImageEdit.route('/bookImageEdit/editBook' , methods=['POST'])
def insertTBbook():
    titleName = request.form['titleName']
    contentTxt = request.form['contentTxt']
    result = 0
    try:
        db = dbBookImageEdit()
        result = db.InsetBook(titleName,contentTxt)
        message = ['保存失败','保存完了'][result > 0]
    except :
        pass
    if result> 0:
        return redirect(url_for('show.showpage',msg = '8'))





######################
@bookImageEdit.route('/fileUp', methods=['POST'])
@admin_request
def upLoad():
    file = request.files['file']
    fileSize = len(file.read())
    if float(fileSize) > config.MAX_CONTENT_LENGTH:
            Showmessage = '文件过大'
            return render_template('Backstage.html',
                title ='流年暗渡',
                url = '',
                Showmessage = Showmessage)
    else:
        if file and allowed_file(file.filename):

            #fileName = secure_filename(file.filename)
            #fileName = r_slash(file.filename) 
            dt = str(datetime.now().timestamp() /1000).replace('.','')  + str(random.randint(1,100))
            fileName = dt + getFileType(file.filename)
            size = (500,333)
            im = Image.open(file)
            im.thumbnail(size)
            try:
                im.save(os.path.join(config.UPLOAD_FOLDER,fileName))          # 保存到路径
                #file_url = config.UPLOAD_FOLDER + '\\'+ fileName
                file_url = url_for('bookImageEdit.uploaded_file', filename = fileName)   # 获取上传的文件
            except Exception  as e:
                errorlog = dbErrorLog()
                errorlog.errorLog(e,'savepicture')
                
            
            title = request.form['titleshow']
            conntent = request.form['contentshow']
            try:
                db = dbBookImageEdit()
                result = db.InsetShow(fileName,title,conntent,file_url)
                Showmessage = ['保存失败','保存完了'][result > 0]
            except Exception  as e:
                errorlog = dbErrorLog()
                errorlog.errorLog(e,'insetPicture')
        
            return render_template('BookImageEdit.html',
                 title ='流年暗渡',
                 url = file_url,
                 Showmessage = Showmessage)
        else:
            return render_template(
                'BookImageEdit.html',
                title='流年暗渡',
                Showmessage ='文件格式不正确',
                )

@bookImageEdit.route('/fileUp/<filename>')
def uploaded_file(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename)

#检查文件名称判断是否图片
def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.',1)[1] in config.ALLOWED_EXTENSIONS

#后缀
def getFileType(filename):
    return  '.'+ filename.rsplit('.',1)[1]
    