# -*- coding: utf-8 -*-
import socket
import urllib.request
import http.cookiejar
# user_agent = {'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
# file = urllib.request.urlopen('http://www.baidu.com')
import time

import lxml.html
import re
import urllib.error
import os

'''
URL异常处理神器URLError
可以用下面的方法来处理任何方式的url异常
    try:
        data = urllib.request.urlopen('http://blog.csdn.net')
        print(len(data.read()), data.status)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

以下为http状态码：
一、200状态码： 
　　成功2××： 成功处理了请求的状态码。 
　　1、200 ：服务器已成功处理了请求并提供了请求的网页。 
　　2、204： 服务器成功处理了请求，但没有返回任何内容。 
二、300状态码： 
　　重定向3×× ：每次请求中使用重定向不要超过 5 次。 
　　1、301： 请求的网页已永久移动到新位置。当URLs发生变化时，使用301代码。搜索引擎索引中保存新的URL。 
　　2、302： 请求的网页临时移动到新位置。搜索引擎索引中保存原来的URL。 
　　3、304： 如果网页自请求者上次请求后没有更新，则用304代码告诉搜索引擎机器人，可节省带宽和开销。 
三、400状态码： 
　　客户端错误4×× ：表示请求可能出错，妨碍了服务器的处理。 
　　1、400： 服务器不理解请求的语法。 
　　2、403： 服务器拒绝请求。 
　　3、404： 服务器找不到请求的网页。服务器上不存在的网页经常会返回此代码。 
　　4、410 ：请求的资源永久删除后，服务器返回此响应。该代码与 404（未找到）代码相似，但在资源以前存在而现在不存在的情况下，有时用来替代404 代码。如果资源已永久删除，应当使用 301 指定资源的新位置。 
四、500状态码： 
　　服务器错误5×× ：表示服务器在处理请求时发生内部错误。这些错误可能是服务器本身的错误，而不是请求出错。 
　　1、500 ：服务器遇到错误，无法完成请求。 
　　2、503： 服务器目前无法使用（由于超载或停机维护）。
　　通常，这只是暂时状态。 希望大家在分析日志的时候可以参照一下，根据具体的状态码解决问题。
'''


import subprocess

import requests
from requests.exceptions import ProxyError


def get_proxies(url='', cssselect=''):
    '''
    返回网站上抓到的代理地址
    :param url:
    :param cssselect:
    :return:
    '''
    # 用以下3行代码来修复可能不完整的html
    url = 'http://www.xicidaili.com/nn/'
    bronk_html = get_html(url)
    import lxml.html
    tree = lxml.html.fromstring(bronk_html)
    # print(bronk_html)
    # fixed_html = lxml.html.tostring(tree, pretty_print=True)
    # 用lxml的css选择器来抽取需要的数据
    tds = tree.cssselect('tr td')
    total = len(tds)
    ippat = r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'
    portpat = r'[0-9]{1,5}\d$'
    typepat = r'[HTTP|HTTPS]'
    ips = []
    ports = []
    types = []
    http = []
    https = []
    for i in tds:

        try:
            ip = re.compile(ippat).match(i.text)
            if ip:
                ips.append(i.text)
                # print(i.text)
            port = re.compile(portpat).match(i.text)
            if port:
                ports.append(i.text)
                # print(i.text)

            type = re.compile(typepat).match(i.text)
            if type:
                types.append(i.text)
                # print(i.text)
        except Exception as e:
            # print(e)
            pass


    def is_ip_available(proxy_ip):
        #subprocess.getstatusoutput 第一个参数获得状态，第二个获得输出
        print('testing {}'.format(proxy_ip))
        flag = subprocess.getstatusoutput('ping -c 1 {}'.format(proxy_ip))# 可用返回0,不可用256
        if flag:
            return True

    for ip, port, type in zip(ips, ports, types):
        # infos.append((ip, port, type))
        # print({type: ':'.join([ip, port])})
        if type == 'HTTP':
            http.append(':'.join([ip, port]))
        elif type == 'HTTPS':
            https.append(':'.join([ip, port]))
    return (http, https)

def get_html(url=''):

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')

    # for i in range(1, 1000):
    try:
        print('getting html...')
        data = urllib.request.urlopen(url=req, timeout=30)
        print('get html done.')
        return data.read().decode('utf8')
    except Exception as e:
        print(e)
        # if hasattr(e, 'code'):
        #     print(e.code)
        #     if e.code == 429:
        #         print('sleep 30 seconds.')
        #         time.sleep(30)

def write_to_file(data=None, path=''):
    if not data:
        return None
    try:
        with open(path, 'w') as f:
            f.write(data)
            print('wirte data to {} is done.'.format(path))
    except Exception as e:
        print(type(e))
        print(e)
        with open(path, 'wb') as f:
            f.write(data)
            print('wirte data to {} is done.'.format(path))
def test_get():
    '''
    test GET
    :return:
    '''
    key_word = '张三'
    #如果关键字为中文需要用urllib.request.quote 转码
    url = 'https://www.baidu.com/s?wd={}'.format(urllib.request.quote(key_word))
    print(url)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    try:
        data = urllib.request.urlopen(req, timeout=20)
        write_to_file(data.read().decode('utf8'))
    except Exception as e:
        print(e)
    print(data.read().decode('utf8'))
    pass


def test_post():
    '''
    测试POST
    关键在于分析form表单将需要的数据装入字典，然后用urllib.parseurlencode（）编码处理，在encode（‘utf8’）
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    url = 'http://iqianyue.com/mypost/'
    #将数据用urlencode转码后再用encode编码
    postdata = urllib.parse.urlencode(
        {
            'name': 'alex',
            'pass': 'test',
        }
    ).encode('utf8')
    req = urllib.request.Request(url=url, data=postdata, headers=headers)
    data = urllib.request.urlopen(req)

    print(data.read().decode('utf8'))

    pass

def use_proxy(url='', proxies=''):
    '''
    urllib 使用代理
    :param url:
    :param proxies:
    :return:
    '''
    proxyaddr = '115.28.214.174:8081'
    #设置代理handler
    proxy = urllib.request.ProxyHandler({'http': proxyaddr})
    print('opener')
    #用handler添加header的时候要用 元组 而不是 字典
    header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    http_handler = urllib.request.HTTPHandler(debuglevel=1)
    https_handler = urllib.request.HTTPSHandler(debuglevel=1)
    #创建opener
    opener = urllib.request.build_opener(proxy, http_handler, https_handler)
    # opener = urllib.request.build_opener(http_handler, https_handler)
    opener.addheaders = [header]
    #创建全局默认的opener对象，这样使用urlopen的时候就会使用install的opener
    urllib.request.install_opener(opener)
    print('get data')
    data = urllib.request.urlopen(url).read().decode('utf8')
    print('after get data')
    return data

def test_cookie():
    '''
    无cookie的测试
    打开url2的时候没有登录状态
    :return:
    '''
    header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')

    a = {
        'username': 'alexzt332211',
        'password': 'Aa123456!'
    }

    url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LCTqO'
    postdata = urllib.parse.urlencode(a).encode('utf-8')
    req = urllib.request.Request(url, postdata)
    req.add_header = header

    data = urllib.request.urlopen(req).read()

    write_to_file(data, path='test.html')

    url2 = 'http://bbs.chinaunix.net/'
    req2 = urllib.request.Request(url2, postdata)
    req2.add_header = header
    data2 = urllib.request.urlopen(req2).read()

    write_to_file(data2, 'test2.html')


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data



def test_cookie2():
    '''
    用http.cookiejar模块来处理cookie，这样就能保留住登录状态
    如下该步骤：
    1，导入http.cookiejar
    2，使用http.cookiejar.CookieJar()创建cookiejar对象
    3,使用HTTPCookieProcessor来创建cookie处理器，并一起为参数构建opener对象
    4,将opener安装为全局
    :return:
    '''
    header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    #chinaunxi 帐号密码
    a = {
        'username': 'alexzt332211',
        'password': 'Aa123456!'
    }
    url = 'http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LCTqO'
    #chinaunix
    postdata = urllib.parse.urlencode(a).encode('utf-8')
    print('1')
    req = urllib.request.Request(url, postdata)
    print('2')

    req.add_header = header
    print('3')

    #实例化cookiejar对象
    cjar = http.cookiejar.CookieJar()
    print('4')

    #使用HTTPCookieProcessor来创建cookie处理器，并一起为参数构建opener对象
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    print('5')

    #将opener安装为全局
    urllib.request.install_opener(opener)
    print('6')
    file = opener.open(req)
    print('7')
    data = file.read()
    print('8')
    write_to_file(data, 'test1.html')
    url2 = 'http://bbs.chinaunix.net/'
    data2 = urllib.request.urlopen(url2).read()
    write_to_file(data2, 'test2.html')


def test_cookie3():
    '''
    一
    用http.cookiejar模块来处理cookie，这样就能保留住登录状态
    如下该步骤：
    1，导入http.cookiejar
    2，使用http.cookiejar.CookieJar()创建cookiejar对象
    3,使用HTTPCookieProcessor来创建cookie处理器，并一起为参数构建opener对象
    4,将opener安装为全局

    二
    example.webscraping.com这个网站form表单中有隐藏的input
    而且据书上所说是存在cookie中的
    先执行步骤一安装全局opener，用其打开页面就可以将隐藏的input保存在cookie中
    这里的方法是用一个函数把form表单中的input中的name和value取出来
    然后封装form表单参数传给urlencode再继续执行以后的步骤



    :return:
    '''


    #实例化cookiejar对象
    cjar = http.cookiejar.CookieJar()
    print('1')

    #使用HTTPCookieProcessor来创建cookie处理器，并一起为参数构建opener对象
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    print('2')

    #将opener安装为全局
    urllib.request.install_opener(opener)
    print('3')
    header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    #chinaunxi 帐号密码

    url = 'http://example.webscraping.com/places/default/user/login'
    html = opener.open(url).read()
    # print(html)
    formdata = parse_form(html)
    print(formdata)
    a = {
        'email': '110021341@qq.com',
        'password': 'AA123456',
        '_next': '/places/default/index',
        '_formname': 'login',
        '_formkey': formdata['_formkey']
    }
    postdata = urllib.parse.urlencode(a).encode('utf-8')
    print('4')
    req = urllib.request.Request(url, postdata)
    print('5')
    req.add_header = header
    print('6')
    response = opener.open(req)
    print('7')
    # print(response.geturl())
    data = response.read()
    print('8')
    write_to_file(data, 'test1.html')
    url2 = 'http://example.webscraping.com/'
    data2 = urllib.request.urlopen(url2).read()
    write_to_file(data2, 'test2.html')


def test_jd():
    '''
    JD测试爬虫程序
    下载手机页面的指定数量的图片
    用正则过滤文档
    注意？的使用很关键
    :return:
    '''
    pages = 20
    for page in range(1, pages-1):
        # time.sleep(5)
        url = 'https://list.jd.com/list.html?cat=9987,653,655&page={}'.format(page)
        ''
        #正则最好前面加r原样输出
        pattern = r'<div id="plist".+? <div class="page clearfix">'

        # header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
        header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0', }

        req = urllib.request.Request(url)
        #获得页面
        #JD的页面很怪，html代码和爬到的html不一样要分析一下下载到的代码来查找链接
        html1 = urllib.request.urlopen(req).read()


        # print(html1.decode('utf8'))
        #转换为str不能显示中文如果需要，用decode函数
        html1 = str(html1)
        #用第一个re过滤页面找到具体的div
        result1 = re.compile(pattern).findall(html1)[0]
        #待理解 为什么加一个？ 贪婪0或多个字符就可以正确的获得所有地址
        pat2 = r'<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)">'
        imagelist = re.compile(pat2).findall(result1)
        current_dir = 'test/{}'.format(page)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        for i in imagelist:
            link = 'http://' + i
            # if os.path.exists(current_dir + '/' + i.split('/')[-1]):
            #     continue
            try:
                urllib.request.urlretrieve(link, filename='test/{}/{}'.format(page, i.split('/')[-1]))
            except Exception as e:
                print(type(e))
                print(e)

def qiushibaike(url=''):
    header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
    opener = urllib.request.build_opener()
    opener.addheaders = [header]
    urllib.request.install_opener(opener)

    html = urllib.request.urlopen(url).read().decode('utf8')

    namepat = r'<h2>\s(.*?)\s</h2>'
    names = re.compile(namepat).findall(html)
    contentpat = r'<div class="content">\s<span>([\s\S]*?)</span>\n+?</div>'
    contents = re.compile(contentpat).findall(html)
    result = {}
    for key, val in zip(names, contents):
        # print(key, val)
        result.update({key: val.replace('\n', '')})
    return result

class WxTest():
    def __init__(self, key='', pagestart=1, pageend=1 ,proxies=None,use_proxy=True):
        self.headers = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [self.headers]
        self.listurl = []
        # self.proxies = {'http': '110.72.40.183:8123', 'https': '112.114.97.62:8118'}
        self.proxies = proxies
        urllib.request.install_opener(self.opener)
        self.getlinks(key=key, pagestart=pagestart, pageend=pageend)
        self.use_proxy = use_proxy
        # self.getCotents()

    def use_proxy(self, proxy_addr, url):
        '''
        需要完善次函数
        使用代理获得数据
        :param proxy_addr:
        :param url:
        :return:
        '''
        print('in use_proxy {}'.format(self.proxies) )
        try:
            if self.use_proxy:
                # 注册handleer
                proxy = urllib.request.ProxyHandler(proxy_addr)
                # 实例化opener 添加 代理 与 handler
                opener = urllib.request.build_opener(proxy)
                opener.addheaders = [self.headers]
                urllib.request.install_opener(opener)
            else:
                # 实例化opener
                opener = urllib.request.build_opener()
                opener.addheaders = [self.headers]
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
            time.sleep(5)
        except Exception as e:
            print('2')
            print(type(e))
            print(e)
            time.sleep(1)

    def parse_link(self, html):
        #过滤链接（要注意的是这里parse过来的链接不能直接打开，对比手动打开的链接后分析后发现字段中多了几个阿妈amp;）
        apat = r'<a target="_blank" href="(.*?)"'
        temp = re.compile(apat).findall(html)
        for i in temp:
            print(i)
            self.listurl.append(re.sub('amp;', '', i))


    def getlinks(self, key='', pagestart=1, pageend=1):
        '''
        根据参数来循环获得weixin.sogou的关键词信息
        要注意用urllib.request.quote()来编码key与变量名&page
        :param key:
        :param pagestart:
        :param pageend:
        :return:
        '''
        try:
            #编码关键词与&page
            keycode = urllib.request.quote(key)
            # pagecode = urllib.request.quote('&page')

            #循环爬取个page内的链接
            for page in range(pagestart, pageend + 1):
                url = 'http://weixin.sogou.com/weixin?type=2&query={}&page={}'.format(keycode, page)
                print(url)
                #用代理来获得html
                html = self.use_proxy(self.proxies, url)
                # print(html)
                self.parse_link(html)

        except Exception as e:
            print(type(e))
            print(e)

    def getCotents(self):

        # try:
        for idnex, url in enumerate(self.listurl):
            print(url)
            html = self.use_proxy(self.proxies, url=url)
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
            # print('正在处理{}/{}'.format(idnex + 1 ,len(self.listurl)))
        # except Exception as e:
        #
        #     print(type(e))
        #     print(e)


import threading


class A(threading.Thread):
    def __init__(self):
        # 初始化线程
        threading.Thread.__init__(self)

    def run(self):
        # 该线程的主要内容
        for i in range(100):
            print('我是线程A')

class B(threading.Thread):
    def __init__(self):
        # 初始化线程
        threading.Thread.__init__(self)

    def run(self):
        # 该线程的主要内容
        for i in range(50):
            print('我是线程B')







if __name__ == '__main__':



    #----------多线程测试---------------
    # t1 = A()
    # t1.start()
    # t2 = B()
    # t2.start()

    # import queue
    # q = queue.Queue()
    #
    # q.put('a')
    # q.task_done()
    # q.put('b')
    # q.task_done()
    # q.put('c')
    # q.task_done()
    #
    # for i in range(3):
    #     print(q.get())










    #--------------测试微信------------------
    # http, https = get_proxies()
    # from random import choice
    #
    # proxies = {
    #     'http': choice(http),
    #     'https': choice(https)
    # }
    # wx = WxTest(key='物联网', pagestart=1, pageend=2 ,use_proxy=False)
    # print(len(wx.listurl))





    #-----------------test----------------------
    # url = 'http://www.ip.cn/'
    #
    # http, https = get_proxies()
    # from random import choice
    #
    # proxies = {
    #     'http': choice(http),
    #     'https': choice(https)
    # }
    # print(proxies)
    # a = use_proxy(proxy_addr=proxies, url=url)
    # print(a)










    # #-----------糗事百科测试--------------
    # result = {}
    # length = 13
    # for page in range(1, length + 1):
    #     url = 'https://www.qiushibaike.com/text/page/{}/'.format(page)
    #     result.update(qiushibaike(url))
    #     print('{}/{}'.format(str(page), str(length)))
    #
    #
    # for i in enumerate(result.items()):
    #     print(i)
    # #------------end of test------------

    # get_proxies()
    pass