import json
import urllib.request
import http.cookiejar

#headers dict
import re



def test_vqq_comment():
    '''
    主要实现伪装浏览器技术，此例为伪装headers
    测试爬取v.qq.com的评论，与书上的js取得的有差异
    需要再次测试
    除了获取JS别的没问题
    最终用火狐浏览器F12截取到js地址 将显示个数调整为100 已获取全部的评论
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Accept-Encoding': 'gzip, deflate',#如果用压缩的话服务器返回的信息未解压缩会造成乱码，置空就可以了
        'Accept-Encoding': '',
        'Connection': 'keep-alive',
        # 'referer': 'http://www.163.com',
        'referer': 'qq.com',


    }
    vid = '2292665416'
    id = 1514688387714
    # url = 'https://video.coral.qq.com/varticle/2292665416/comment/v2?callback=jQuery112400702184889096632_1514714343192&orinum=100&oriorder=o&pageflag=1&cursor=6347276599490743571&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1514714343199'
    # url = 'https://video.coral.qq.com/varticle/2272484011/comment/v2?callback=jQuery112400702184889096632_1514714343192&orinum=100&oriorder=o&pageflag=1&cursor=6347276599490743571&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1514714343199'
    url = 'https://video.coral.qq.com/varticle/2272484011/comment/v2?callback=jQuery112408890571767520803_1514733056920&orinum=100&oriorder=o&pageflag=1&cursor=6343477131960081310&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1514733056924'
    # url = 'http://news.163.com/17/1230/22/D6UJ7H630001875N.html'
    #设置cookie 待查作用
    cjar = http.cookiejar.CookieJar()
    #使用fiddler代理用来抓包
    #需要url以/结尾，比如http://www.baidu.com 需要尾部加/ http://www.baidu.com/
    #尤菊提页面的直接输入就行类似url这用
    #如果不需要fiddler抓包可以不设置此代理
    prorxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8888'})
    #构建opener
    opener = urllib.request.build_opener(prorxy,
                                         urllib.request.HTTPHandler,
                                         urllib.request.HTTPCookieProcessor(cjar)
                                         )


    headall = []
    #通过循环讲headers 构建headall的信息

    for key, val in headers.items():
        headall.append((key, val))

    print(headall)



    opener.addheaders = headall
    #安装全局opener
    urllib.request.install_opener(opener)

    data = urllib.request.urlopen(url).read().decode('utf8')

    contentpat = r'"content":"(.*?)"'
    nickpat = r'"nick":"(.*?)"'


    contents = re.compile(contentpat).findall(data)
    nicks = re.compile(nickpat).findall(data)
    '''
    eval()的用处
    可以把list,tuple,dict和string相互转化。
    #################################################
    字符串转换成列表
    >>>a = "[[1,2], [3,4], [5,6], [7,8], [9,0]]"
    >>>type(a)
    <type 'str'>
    >>> b = eval(a)
    >>> print b
    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 0]]
    >>> type(b)
    <type 'list'>
    #################################################
    字符串转换成字典
    >>> a = "{1: 'a', 2: 'b'}"
    >>> type(a)
    <type 'str'>
    >>> b = eval(a)
    >>> print b
    {1: 'a', 2: 'b'}
    >>> type(b)
    <type 'dict'>
    #################################################
    字符串转换成元组
    >>> a = "([1,2], [3,4], [5,6], [7,8], (9,0))"
    >>> type(a)
    <type 'str'>
    >>> b = eval(a)
    >>> print b
    ([1, 2], [3, 4], [5, 6], [7, 8], (9, 0))
    >>> type(b)
    <type 'tuple'>'''
    # print(type(nicks))
    # print(nicks)

    def covert(u):
        return eval('u"' + u + '"')

    try:
        infos = ['{}:{}'.format(nick, content) for nick, content in zip(nicks, contents)]
    except Exception as e:
        print(e)
    # print(infos)


    #用eval讲unicode变量转换为字符串输出
    for index, info in enumerate(infos):

        # b = eval('u"' + str(index) + ':' + info + '"')
        try:
            print(index, covert(info).strip())
        except Exception as e:
            print(e)
            print(info)

    # print(data)



if __name__ == '__main__':

    test_vqq_comment()