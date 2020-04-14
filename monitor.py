# -*- coding:utf-8 -*-  
import time
import db
import mailalert
from visit import visit_site

import log
logger = log.logging.getLogger("monitor")

url_task = {}

def tstamp():
    return int(time.time())

def update_urltask():
    global url_task
    # 更新URL列表时间
    db_result = db.url_get()
    if db_result is False:
        return
    for d in db_result:
        urlid, name, url, method, postdata, status, keyword, timeout, integer, createtime = d
        # print(d)
        if url_task.get(urlid, False):
            # 更新
            url_task.get(urlid).update(name=name,
                url=url,
                method=method,
                postdata=postdata,
                status=status,
                keyword=keyword,
                integer=integer,
                timeout=timeout)
        else:
            # 新增
            url_task.setdefault(urlid,{})
            url_task.get(urlid).update(name=name,
                url=url,
                method=method,
                postdata=postdata,
                status=status,
                keyword=keyword,
                integer=integer,
                timeout=timeout,
                visittime=0)


def run_monitor():
    global url_task
    logger.info("monitro start")
    update_urltask()
    start_T = tstamp()
    while True:
        # logger.info("checking")
        # 监控网站
        logger.debug(url_task)
        for k,v in url_task.items():
            check_site(k,v)

        time.sleep(1)
        end_t = tstamp()
        if end_t - start_T >= 30:
            # 每隔30秒更新URL列表
            logger.debug("update url task:")
            start_T = end_t
            update_urltask()
        

def check_site(uid, urlinfo):
    # 校验网站访问是否需要
    lasttime = urlinfo.get("visittime")

    now = tstamp()
    if now - lasttime <= urlinfo.get('integer'):
        # 未过间隔期
        return
    urlinfo.update(visittime=tstamp())
    success, code, keyresult, spendtime = visit_site(urlinfo.get('url'), urlinfo.get('method'), urlinfo.get('postdata'))
    result = ''
    logger.info("URL:{}, 返回码:{}, 匹配结果:{}, 耗时:{}".format(urlinfo.get('url'), code, keyresult, spendtime))
    url_status, key_status, t_status, err_status = 0,0,0,0

    if success:
        if urlinfo.get('status') == code:
            # 代码一致
            url_status = 1000
            result += 'code ok.'
        else:
            url_status = 2000
            result += 'error code:{}!'.format(code)

        if urlinfo.get('keyword') != '':
            if keyresult:
                # 关键词
                key_status = 10
                result += 'keyword ok.'
            else:
                key_status = 20
                result += 'can\'t find keyword!'

        if urlinfo.get('timeout') != '':
            if spendtime < urlinfo.get('timeout'):
                t_status = 1
                result += 'time ok.'
            else:
                t_status = 2
                result += 'timeout!'
    else:
        if code == 0:
            err_status = -1
            result += "can't open url!"
        else:
            pass
    status = url_status + key_status + t_status + err_status
    logger.info("uid:{},status:{}".format(uid, status))
    visitinfo = [uid, spendtime, code, result, status, tstamp()]
    db.visit_history_insert(visitinfo)
    if url_status>1000 or key_status>10 or t_status>1:
        # 异常发送邮件或者短信提醒
        title = "website visit exception:{}".format(urlinfo.get('name'))
        message = "status:{}\nurl:{}\nmessage:\n{}".format(status, urlinfo.get('url'), result)
        alert_email(uid, urlinfo.get('url'), title, message)


email_last_sendtime = 0 # 上一次发送告警邮件时间,用于控制发送邮件间隔。

def alert_email(uid, url, title, message):
    # touch alert, event status: 1 send sucess 2 mail fail 3 error mail address 4 interval time not out
    global email_last_sendtime
    status = 0
    if tstamp() - email_last_sendtime > 1500:
        # send email every 15 minutes
        db.delete_old_data() # Delete old data every 15 minutes
        email_last_sendtime = tstamp()
        reciver_address = [b[3] for b in db.user_get()]
        if len(reciver_address) == 0:
            logger.warning("reciver email is empty!")
            # uid, url, result, status, createtime
            db.event_insert([uid, url, message, 3, tstamp()])
            return
        success, errmsg = mailalert.send_email(title, message, reciver_address)
        # success = True
        # errmsg ='ok'
        logger.info("send email:{}\n{}\n{}\n{}\n{}".format(success, errmsg, title, reciver_address, message))

        if success:
            # 发送成功
            db.event_insert([uid, url, message, 1, tstamp()])
            
        else:
            db.event_insert([uid, url, message, 2, tstamp()])
    else:
        # 未超过发送邮件间隔,发送邮件.控制邮件间隔
        db.event_insert([uid, url, message, 4, tstamp()])
 

if __name__ == '__main__':
    run_monitor()
    # pass
    # run_monitor()
    # print(url_task)
    # print(15*60)

    # result = db.user_get()
    # for i in result:
    #     _,_,_,address,_,_ = i
    #     print(address)
    # print(result)
    # print([b[3] for b in db.user_get()])
    # alert_email(1,'xxx.com', "site check","site warning to team")