
# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, g, request 
from datetime import datetime
import math
from main.dbCon.dbShowBook import dbShowBook
from main.showBook import show

@show.route('/show', methods =['POST','GET'] )
def showpage():
    avgNum = 5  #每页显示数目
    p = request.args.get("p")  #页码
    show_first_statue = 0  #首页状态    
    if p is None:
        p = 1
    else:
        p = int(p)
        if p > 1:
            show_first_statue = 1

    limit_start = (int(p) -1) * avgNum #起始页码 每页5条

    conn = dbShowBook()
    bookList = conn.ReadBook(limit_start)
    count = conn.TotleBookNum()  #总数
    totalPage = int(math.ceil(count/avgNum)) #总页数

    dic = getPage(totalPage, p)
    return render_template(
        'showBook.html',
        title = '星庐听雨',
        bookList = bookList,
        p = int(p),
        totalPage = totalPage,
        show_first_statue = show_first_statue,
        dic_list = dic
        ).encode('utf-8')

def getPage(total, p):
    show_page = 5   #控件显示的 块
    pageoffset = 2
    start =1
    end = total

    if total> show_page:
        if p>pageoffset:
            start = p - pageoffset
            if total > p + pageoffset:
                end = p + pageoffset
            else:
                end = total
        else:
            start =1
            if total > show_page:
                end = show_page
            else :
                end = total
        if p + pageoffset > total:
            start = start -(p + pageoffset - end)
    dic = range(start, end+1)
    return dic