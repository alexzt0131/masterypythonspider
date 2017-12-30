# def __init__(key='', pagestart=1, pageend=1, proxies=None, use_proxy=True):
#     headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
#     opener = urllib.request.build_opener()
#     opener.addheaders = [headers]
#     listurl = []
#     # proxies = {'http': '110.72.40.183:8123', 'https': '112.114.97.62:8118'}
#     proxies = proxies
#     urllib.request.install_opener(opener)
#     getlinks(key=key, pagestart=pagestart, pageend=pageend)
#     use_proxy = use_proxy
#     # getCotents()
import queue
import urllib.request
import time
import re
import threading
import urllib.error


def use_proxy(proxy_addr, url, use_proxy=False):
    '''
    需要完善次函数
    使用代理获得数据
    :param proxy_addr:
    :param url:
    :return:
    '''
    print('in use_proxy {}'.format(proxy_addr))
    headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    try:
        if use_proxy:
            # 注册handleer
            proxy = urllib.request.ProxyHandler(proxy_addr)
            # 实例化opener 添加 代理 与 handler
            opener = urllib.request.build_opener(proxy)
            opener.addheaders = [headers]
            urllib.request.install_opener(opener)
        else:
            # 实例化opener
            opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            urllib.request.install_opener(opener)
        try:
            data = urllib.request.urlopen(url).read().decode('utf8')
        except UnicodeDecodeError as e:
            print(e)
            data = urllib.request.urlopen(url).read().decode('gbk')
        except Exception as e:
            print(type(e))
            print(e)
        return data
    except urllib.error.URLError as e:
        print('1')
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
        print('sleep 10 seconds')
        time.sleep(10)
    except Exception as e:
        print('2')
        print(type(e))
        print(e)
        time.sleep(1)


# def parse_link(html):
#     # 过滤链接（要注意的是这里parse过来的链接不能直接打开，对比手动打开的链接后分析后发现字段中多了几个阿妈amp;）
#     apat = r'<a target="_blank" href="(.*?)"'
#     temp = re.compile(apat).findall(html)
#     for i in temp:
#         # print(i)
#         return re.sub('amp;', '', i)

class GetLinks(threading.Thread):

    def __init__(self, key='', proxies='', pagestart=1, pageend=1, urlqueue=None, use_proxy=False):
        #多线程固定格式调用threading.Thread.__init__(self)
        threading.Thread.__init__(self)
        self.key = key
        self.pagestart = pagestart
        self.pageend = pageend
        self.use_proxy = use_proxy
        self.proxies = proxies
    def run(self):
        # try:
        # 编码关键词与&page
        keycode = urllib.request.quote(self.key)
        # pagecode = urllib.request.quote('&page')

        # 循环爬取个page内的链接
        for page in range(self.pagestart, self.pageend + 1):
            url = 'http://weixin.sogou.com/weixin?type=2&query={}&page={}'.format(keycode, page)
            # print(url)
            if use_proxy:
                # 用代理来获得html
                html = use_proxy(self.proxies, url, use_proxy=True)
            else:
                html = use_proxy(None, url, use_proxy=False)
            print(type(html))
            print(len(html))
            print(html)
            try:
                apat = r'<a target="_blank" href="(.*?)"'
                urls = re.compile(apat).findall(html)
                for url in urls:
                    # 将url加入队列
                    urlqueue.put(url)
                    urlqueue.task_done()
            except Exception as e:
                print(e)
                pass

        # except Exception as e:
        #     print(type(e))
        #     print(e)


def getCotents(self):
    # try:
    for idnex, url in enumerate(listurl):
        print(url)
        html = use_proxy(proxies, url=url)
        content = lxml.html.fromstring(html).cssselect('#js_content')[0]
        titlepat = r'<title>(.*)</title>'
        title = re.compile(titlepat).findall(html)
        filename = title
        print(title)
        print(content)
        break
        top = '''
           <!DOCTYPE html>
       <html lang="en">
       <head>
           <meta charset="UTF-8">
           <title>{}</title>
       </head>
       <body>
           '''.format(title)
        foot = '''
       </body>
       </html>
           '''
        # with open('{}.html'.format(filename), 'w+') as f:
        #     f.write(top)
        # with open('{}.html'.format(filename), 'ab') as f:
        #     f.write(content.strip().encode('utf8'))
        # with open('{}.html'.format(filename), 'a') as f:
        #     f.write(foot)
        # print('正在处理{}/{}'.format(idnex + 1 ,len(listurl)))
    # except Exception as e:
    #
    #     print(type(e))
    #     print(e)


if __name__ == '__main__':

    #已完成递归获得所有页面地址，需要研究好的使用代理的方法
    #最后在获取页面中的信息
    #--------------多线程测试-------------------
    headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    listurl = []
    # proxies = {'http': '110.72.40.183:8123', 'https': '112.114.97.62:8118'}
    proxies = ''
    urllib.request.install_opener(opener)
    urlqueue = queue.Queue()

    t1 = GetLinks(key='人工智能', proxies={'http': '114.212.80.2:9999'}, urlqueue=urlqueue, use_proxy=True)
    t1.start()
    print('--'*88)
    print(urlqueue.empty())
    while not urlqueue.empty():
        print(urlqueue.put())



    pass
