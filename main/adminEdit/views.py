

from flask import Blueprint, render_template, request 
import re
from main.dbCon.dbAdminEdit import dbAdminEdit
from main.pubCore.userVerification import Superadmin_request

from main.adminEdit import adminEdit


@adminEdit.route('/adminEdit')
@Superadmin_request
def Default():
    return render_template(
         'AdminEdit.html',
         title= '秋霜飞晚',
         dataList = '',
        )


@adminEdit.route('/adminEdit/startdb', methods =['POST'])
def startdb():
    tablename = ''
    cloumList = request.form.to_dict()
    getList = []
    for (key, value) in cloumList.items():
        if re.match(r'tablename',key):
            tablename = value
        if re.match(r'careateCloum',key):
            getList.append(value)
    if tablename != '' and len(getList) > 0 :
        conn = dbAdminEdit()
        conn.creatTable(tablename,getList)
    return render_template(
            'AdminEdit.html',
            title = '秋霜飞晚',
            message = 'Create is ok',
            dataList = '',
        ).encode('utf-8')

@adminEdit.route('/adminEdit/insertdb', methods=['POST'])
def insertData():
    
    tableText = request.form['sqlText']
    if tableText!= '':
        conn = dbAdminEdit()
        num = conn.inster(tableText)
        givemessage = ['操作完了 自行检查数据']
    return render_template(
            'AdminEdit.html',
            title = '秋霜飞晚',
            message = givemessage,
            dataList = '',
        ).encode('utf-8')


@adminEdit.route('/adminEdit/searchdb', methods=['POST'])
def SearchData():
    
    tablename = request.form['tablename']
    if tablename!= '':
        conn = dbAdminEdit()
        fullTable = conn.search(tablename)
    return render_template(
            'AdminEdit.html',
            title = '秋霜飞晚',
            tname = tablename,
            columnList = fullTable[0],
            dataList = fullTable[1],
        ).encode('utf-8')



