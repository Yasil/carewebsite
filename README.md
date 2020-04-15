# 什么是carewebsite
carewebsite,是一个基于python3标准库构建的极简网站和api监控工具，无需安装任何第三方包只要有python3(建议3.5+以上)就可以直接运行。monitor website, monitor api. 网站监控,API监控,接口监控,极简监控 
功能包括如下：
- 按返回码监控
- 按返回值关键字监控
- 按响应时间监控
- 发送预警邮件（后续增加短信|微信|第三方支持）
- web界面管理,支持GET，post方法(post数据格式:{'id':1,"page":1})
- 跨平台  

# 配置和使用 carewebsite
- 1 设置SMPT邮件服务器, 编辑根目录下的config.json,:  
```python
{
  "mail_sender":"xxxx@qq.com", # 发送邮箱地址
  "mail_server":"smtp.qq.com", # smtp邮箱服务器地址
  "mail_server_pw":"fgxxxxxxxa" # 邮箱服务器密码
}
```
  
- 2 运行:  
  - windows:  
      安装python3,运行 python site.py
  - mac:  
      安装python3,运行 python site.py
  - linux:  
      安装python3,运行 python site.py(注意：linux 需要支持ssl和sqlite3. 测试import ssl 和 import sqlite3 是否正常)
  
- 3 使用:   
  1 打开 http://localhost:8080/ 或 http://ip:8080/ , 默认账号admin,密码:123456  
  2 可删除默认账号，新增账号和邮箱（用于预警）  
  3 增加URL监控.  

# carewebsite运行截图
  ![01](https://github.com/Yasil/carewebsite/blob/master/cutimg/20200414101233.png)  
  
  ![02](https://github.com/Yasil/carewebsite/blob/master/cutimg/20200414101319.png)

# FAQ
  有问题或建议请反馈到issues,或者直接pull上来！