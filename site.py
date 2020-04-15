# -*- coding:utf-8 -*-  
import os
from bottle import route, run, template, static_file
from bottle import hook, request, response, get, error, abort, post, redirect
import hashlib
import json
from sitehandler import create_session, check_session, clear_session, check_user, json_resp
from sitehandler import web_get_url, web_get_alert, web_get_user, web_get_history, web_get_urldetail, web_get_url_delete, web_url_add
from sitehandler import web_get_url_delete, web_url_add, web_user_delete, web_user_add, web_alert_empty, web_history_empty

import log
logger = log.logging.getLogger("site")


@hook('before_request')
def validate():
    """
    钩子函数，处理请求路由之前需要做什么的事情
    :return:
    """
    """使用勾子处理页面或接口访问事件"""
    # 让bottle框架支持jquery ajax的RESTful风格的PUT和DELETE等请求
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')
    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD

    # check userlogin
    path_info = request.environ.get("PATH_INFO")

    if request.method == 'OPTIONS':
        # actual request; reply with the actual response
        # print('打印！！！')
        logger.warning("OPTIONS")
        
    # 获取当前访问的Url路径
    # 过滤不用做任何操作的路由
    if path_info in ['/favicon.ico', '/check_err/', '/log/']:
        return ''


@hook('after_request')
def enable_cors():
    """
    钩子函数，处理请求路由之后需要做什么的事情
    :return:
    """
    pass
    # response.headers['Access-Control-Allow-Origin'] = '*'


@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./html/')

@route('/')
def server_default():
    return static_file('/html/login.html', root='./html/')

@route('/index')
def server_default():
    return static_file('index.html', root='./html/')

@route('/hello/<name>')
def index(name):
    session = request.get_cookie('session')
    return template('<b>Hello {{name}}</b>!', name=name)


@post('/logout')
def logout():
    # sessionid = request.get_cookie('session')
    sessionid = request.forms.get("session")
    clear_session(sessionid)
    redirect("/html/login.html")


def check_login():
    sessionid = request.get_cookie('session')
    if sessionid is None:
        # return json_resp(1,"login first")
        # redirect("/html/login.html")
        return json_resp(1,"login first")

    success,errmsg = check_session(sessionid)
    logger.debug("session:{},{},{}".format(sessionid, success, errmsg))
    if success is False:
        # redirect("/html/login.html")
        return json_resp(1, errmsg)

@post('/api/loginpost')
def login():
    name = request.forms.get("username")
    pw = request.forms.get("password")
    if check_user(name, pw):
        # login
        session = create_session(name)
        response.set_cookie('session', session)
        return '{"errcode": 0,"errmsg": "login success","data":"'+ session +'"}'
    else:
        return '''{"errcode": 1,"errmsg": "user not exists or else"}'''

@route('/api/urls')
def urls():
    check_result = check_login()
    if check_result is not None:
        return check_result

    page = request.query.page
    limit = request.query.limit
    count, data = web_get_url(int(page), int(limit))
    return json_resp(0,'ok', count, data)

@route('/api/alerts')
def alerts():
    check_result = check_login()
    if check_result is not None:
        return check_result

    page = request.query.page
    limit = request.query.limit
    count, data = web_get_alert(int(page), int(limit))
    return json_resp(0,'ok', count, data)

@route('/api/users')
def alerts():
    check_result = check_login()
    if check_result is not None:
        return check_result

    page = request.query.page
    limit = request.query.limit
    count, data = web_get_user(int(page), int(limit))
    return json_resp(0,'ok', count, data)


@route('/api/historys')
def alerts():
    check_result = check_login()
    if check_result is not None:
        return check_result

    page = request.query.page
    limit = request.query.limit
    count, data = web_get_history(int(page), int(limit))
    return json_resp(0,'ok', count, data)


@route('/api/urldetail')
def urldetail():
    check_result = check_login()
    if check_result is not None:
        return check_result

    urlid = request.query.id
    count, data = web_get_urldetail(urlid)
    return json_resp(0,'ok', count, data)

@post('/api/url/delete')
def urldetail():
    check_result = check_login()
    if check_result is not None:
        return check_result

    urlid = request.forms.id
    web_get_url_delete(urlid)
    return json_resp(0,'ok')

@post('/api/url/add')
def urladd():
    check_result = check_login()
    if check_result is not None:
        return check_result
    addurl = dict(request.forms)
    name = request.forms.getunicode("name")
    addurl.update(name=name)
    keyword = request.forms.getunicode("keyword")
    addurl.update(keyword=keyword)
    post = request.forms.getunicode("post")
    addurl.update(post=post)
    url = request.forms.getunicode("url")
    addurl.update(url=url)
    web_url_add(addurl)
    return json_resp(0,'ok')

@post('/api/user/delete')
def userdetail():
    check_result = check_login()
    if check_result is not None:
        return check_result

    userid = request.forms.id
    web_user_delete(userid)
    return json_resp(0,'ok')

@post('/api/user/add')
def urladd():
    check_result = check_login()
    if check_result is not None:
        return check_result

    web_user_add(dict(request.forms))
    return json_resp(0,'ok')

@get('/api/alert/empty')
def alertempty():
    check_result = check_login()
    if check_result is not None:
        return check_result

    web_alert_empty()
    return json_resp(0,'ok')

@get('/api/hitory/empty')
def hisempty():
    check_result = check_login()
    if check_result is not None:
        return check_result

    web_history_empty()
    return json_resp(0,'ok')


if __name__ == '__main__':
    from monitor import run_monitor
    import threading
    monitor = threading.Thread(target=run_monitor, args=(), name="monitor")
    monitor.start()
    run(host='', port=8080)


    # print(json_resp(0,"登录成功"))
    # print(get_md5('123456'))
    # print(check_user('admin','123456'))
    # s = create_session("hello")
    # print(s)
    # print(session_dict)
    # import time
    # time.sleep(3)
    # r = check_session(str(s))
    # print(r)
    # print(session_dict)


