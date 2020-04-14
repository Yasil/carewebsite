import hashlib
import time
import json

def get_md5(dstr):
    # return md5
    h = hashlib.md5()
    h.update(dstr.encode('utf-8'))
    return h.hexdigest()

def clock():
    return int(time.time())


def read_config():
    with open('config.json','r') as f:
        config = json.loads(f.read())
        return config


if __name__ == '__main__':
    read_config()
