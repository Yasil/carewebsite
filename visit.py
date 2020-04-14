

from urllib import parse
from urllib import request
from urllib.error import URLError, HTTPError
import time
import log
logger = log.logging.getLogger("visit")


get_now_milli_time = lambda: int(time.time() * 1000)

def visit_site(url, v_type='get', postdata=None, keyword=None):
    # 返回值： 成功|失败, 状态码, 关键字匹配结果, 消耗时间
    try:
        if v_type == 'get':
            r = request.Request(url)
        else:
            encoded_args = parse.urlencode(postdata).encode('utf-8')
            r = request.Request(url,encoded_args)
        r.add_header(
            'User-agent',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        )
        start = get_now_milli_time()
        with request.urlopen(r, timeout=3) as f:
            data = f.read()
            logger.info('Status:{},{}'.format(f.status, f.reason))
            # for k, v in f.getheaders():
            #   print('%s: %s' % (k, v))
            logger.debug('Data:\n{}'.format(data.decode('utf-8')))
    except HTTPError as e:
        end = get_now_milli_time()
        logger.error('{}:Error code:{}'.format(url, e.code))
        return True, e.code, False, end - start
    except URLError as e:
        logger.error('{}:URLError Reason:{}'.format(url, e.reason))
        return False, 0, False, 0
    except ValueError as e:
        logger.error('{}:URL vlaue error:{}'.format(url, e))
        return False, 0, False, 0
    else:
        end = get_now_milli_time()
        logger.info('{}:OK'.format(url))
        if keyword is not None:
            return True, f.status, keyword in data.decode('utf-8'), end - start
        else:
            return True, f.status, False, end - start
    finally:
        pass

if __name__ == '__main__':
    # result = visit_site('http://www.dogedoge.com')
    # print(result)
    # query_args = {'username': 'admin', 'password':'123456'}
    # result = visit_site('http://localhost:8080/api/loginpost', 'post', query_args)
    # print(result)
    pass