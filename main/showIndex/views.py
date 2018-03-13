# -*- coding:utf-8 -*-

from flask import Blueprint , render_template , g 
from datetime import datetime
from main.dbCon.dbindex import dbindex
from main.pubCore.userVerification import login_reques 
import json
import random
from main.showIndex import index

@index.route('/')
@index.route('/home')
#@login_reques
def home():
    username = None
    conn = dbindex()    
    showPicture = conn.showIndex()
    
    return render_template(
        'index.html',
        title = '骤雨逐风',
        year = datetime.now().year,
        showPicture = showPicture,
        ).encode('utf-8')

@index.route('/getjson')
def getJson():
    conn = dbindex()
    optionList = conn.getOptionList()
    showOption = []
    for x in optionList:
        item = {}
        item['name'] = x[1]
        item['value'] = random.randint(100,1000)
        showOption.append(item)
    jsonList = json.dumps(showOption,ensure_ascii=False)
    return jsonList



