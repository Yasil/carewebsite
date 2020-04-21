# -*- coding:utf-8 -*-  
from multiprocessing import Process
from monitor import run_monitor
from adminsite import run_web_site

# import threading
# monitor = threading.Thread(target=run_monitor, args=(), name="monitor")
# monitor.start()
if __name__ == '__main__':
    monitor = Process(target=run_monitor, args=(), name="monitor")
    monitor.start()
    run_web_site()