#coding=utf-8
from smtplib import SMTP_SSL
import log
from tool import read_config

logger = log.logging.getLogger("mail")


def send_email(title, msg, receivers):
    dmail = read_config()
    sender = dmail.get('mail_sender')
    #smtp server
    host_server = dmail.get('mail_server')
    #smtp server pw
    pwd = dmail.get('mail_server_pw')

    message = """From: From Person <{0}>
To: To Person <all@monitor.com>
Subject: {1}

{2}
"""
    try:
        smtp = SMTP_SSL(host_server)
        #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(0)
        smtp.ehlo(host_server)
        smtp.login(sender, pwd)
        message = message.format(sender, title, msg)
        smtp.sendmail(sender, receivers, message)
        smtp.quit()
    except Exception as e:
        logger.error("send email fail:{}".format(e))
        return False, e
    else:
        logger.debug("send email success")
        return True, ''
    finally:
        pass
        # print("结束")

if __name__ == '__main__':
    send_email('site warning', 'site can\'t vists', 'flowdata@qq.com')