import uuid
import db
import json
from tool import get_md5, clock
import log
logger = log.logging.getLogger("sitehandler")

session_dict = {}

COOKIE_KEY = "20monitor20"

def check_session(sessionid):
    # check_login
    global session_dict
    # print(session_dict)
    logger.debug("session:{}".format(session_dict))
    if session_dict.get(sessionid,False) is False:
        # session fail
        return False, "please login!"
    else:
        if clock() - session_dict.get(sessionid).get('lifetime') > 7200:
            session_dict.pop(sessionid)
            return False, "login timeout!"
        else:
            session_dict.get(sessionid).update(lifetime=clock())

            return True, "ok"

def create_session(username):
    global session_dict
    sessionid = str(uuid.uuid4())
    session_dict.setdefault(sessionid, {"name":username, "lifetime":clock()})
    return sessionid

def clear_session(sessionid):
    global session_dict
    logger.debug(sessionid)
    if session_dict.get(sessionid, False) is not False:
        session_dict.pop(sessionid)


def check_user(name, pw):
    result = db.user_get()
    for i in result:
        if name == i['username']:
            if get_md5(pw) == i['password']:
                # user exists
                return True
            else:
                continue
        else:
            continue
    else:
        # user not exists
        return False


def json_resp(code, msg, count=0, data=None):
    ''' return response json '''
    if data is not None:
        d = {"code":code,
            "msg":msg,
            "count":count,
            "data":data}
        return json.dumps(d)
    else:
        d = {"code":code,
            "msg":msg
            }
        return json.dumps(d)


def web_get_url(page,limit):
    page =  page - 1 if page - 1 >= 0 else 0
    result = db.url_get()
    start = page * limit
    end = start + limit
    return len(result), [dict(r) for r in result[start:end]]


def web_get_alert(page,limit):
    page =  page - 1 if page - 1 >= 0 else 0
    result = db.event_get_all()
    start = page * limit
    end = start + limit
    return len(result), [dict(r) for r in result[start:end]]


def web_get_user(page,limit):
    page =  page - 1 if page - 1 >= 0 else 0
    result = db.user_get()
    start = page * limit
    end = start + limit
    return len(result), [dict(r) for r in result[start:end]]


def web_get_history(page,limit):
    page =  page - 1 if page - 1 >= 0 else 0
    result = db.visit_history_all()
    start = page * limit
    end = start + limit
    return len(result), [dict(r) for r in result[start:end]]

def web_get_urldetail(urlid):
    result = db.visit_history_get(urlid)
    return 60, [dict(r) for r in result]

def web_get_url_delete(urlid):
    result = db.url_delete(urlid)
    return result

def web_url_add(formdict):
    formdict.setdefault('createtime', clock())
    result = db.url_insert(formdict)
    return result

def web_user_delete(userid):
    result = db.user_delete(userid)
    return result

def web_user_add(formdict):
    # user dict
    password = formdict.get('password')
    formdict.update(password=get_md5(password))
    formdict.setdefault('createtime', clock())
    result = db.user_insert(formdict)
    return result


def web_alert_empty():
    return db.event_empty()

def web_history_empty():
    return db.visit_empty()

if __name__ == '__main__':
    # result = web_get_urldetail(2)
    # print(result)
    # web_get_url_delete(22)
    pass