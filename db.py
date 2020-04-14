# -*- coding:utf-8 -*-  
import os
import sqlite3
import log
import tool
logger = log.logging.getLogger("db")

db_filename = 'alert.db'

def get_sql_exec(sql, args=None):
    try:
        logger.debug(sql)
        with sqlite3.connect(db_filename) as conn:
            conn.row_factory = sqlite3.Row
            conn.text_factory = str
            cursor = conn.cursor()
            cursor.execute(sql,args if args is not None else ())
            conn.commit()
    except sqlite3.OperationalError as e:
        logger.error("sql:{},error:{}".format(sql,e))
        return []
    else:
        return cursor.fetchall()
    finally:
        pass

def user_get():
    return get_sql_exec("select * from user")

def user_update(arg):
    # 更新用户 arg={'field':'password','value':'pw','id':1}
    if arg.get('field').isalnum():
        return get_sql_exec("update user set {}=:value where id=:id".format(arg.get('field')), arg)
    else:
        logger.error("user_update非法参数")
        return False

def user_delete(userid):
    # 删除用户 userid=1
    return get_sql_exec("delete from user where id=?", [userid])

def user_insert(userinfo):
    # 插入用户 userid=1
    return get_sql_exec("insert into user(username,password,mail,phone,createtime) values(:username,:password,:mail,:phone,:createtime)", userinfo)

def url_get():
    # 获取URL
    return get_sql_exec("select * from url limit 1000")

def url_insert(urlinfo):
    # 插入URL
    return get_sql_exec("insert into url(name,url,method,postdata,status,keyword,timeout,integer,createtime) values(:name,:url,:method,:postdata,:status,:keyword,:timeout,:integer,:createtime)", urlinfo)

def url_delete(urlid):
    # 删除URL
    return get_sql_exec("delete from url where id=?", [urlid])


def visit_history_all():
    # 获取所有
    return get_sql_exec("select * from visit_history order by id desc limit 1000")

def visit_history_get(uid):
    # 获取历史数据最新的60个
    return get_sql_exec("select id,resp_time,status,createtime from visit_history where uid=? order by id desc limit 60", [uid])

def visit_history_insert(visitinfo):
    # 插入访问历史数据
    return get_sql_exec("insert into visit_history(uid, resp_time, resp_code, result, status, createtime) values(?,?,?,?,?,?) ", visitinfo)

def visit_empty():
    # 清空历史访问数据
    return get_sql_exec("delete from visit_history")

def event_get_all():
    # 获取所有告警历史数据
    return get_sql_exec("select * from event order by id desc limit 1000")

def event_get(uid):
    # 获取历史数据最新的30个
    return get_sql_exec("select * from event where uid=? order by id desc limit 10", [uid])

def event_insert(eventinfo):
    # 插入告警历史数据
    return get_sql_exec("insert into event(uid, url, result, status, createtime) values(?,?,?,?,?) ", eventinfo)

def event_empty():
    # 清空告警历史
    return get_sql_exec("delete from event")

def delete_old_data():
    # Auto delete > 48 hours data
    oldtime = tool.clock() - 48*60*60
    get_sql_exec("delete from event where createtime<?", [oldtime])
    get_sql_exec("delete from visit_history where createtime<?", [oldtime])


if __name__ == '__main__':
    # delete_old_data()
    pass
