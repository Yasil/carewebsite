# -*- coding: utf-8 -*-
from smtplib import SMTP_SSL
import email.utils
from email.mime.text import MIMEText
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

    message = MIMEText(msg)
    # message['To'] = email.utils.formataddr(('Recipient','recipient@example.com'))
    message['From'] = email.utils.formataddr(('websiteadmin',sender))
    message['Subject'] = title
    try:
        smtp = SMTP_SSL(host_server)
        #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(0)
        smtp.ehlo(host_server)
        smtp.login(sender, pwd)
        smtp.sendmail('flowdata@qq.com',
                receivers,
                message.as_string())
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
    # send_email('测试错误', '网站访问错误site can\'t vists', ['flowdata@qq.com'])
    pass