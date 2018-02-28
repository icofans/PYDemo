#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

from urllib.request import quote
from urllib import request
from urllib import parse
import string
from bs4 import BeautifulSoup

def search_film(name):
    url = "http://www.anyunjun.cn/so.html?wd=" + name
    search_url = quote(url,string.printable)
    res = request.urlopen(search_url)
    html = res.read().decode("UTF-8")

    # 获取影片资源
    soup = BeautifulSoup(html,'html5lib')
    curl = soup.find_all('a',class_='js-tongjic')

    if len(curl) == 0:
        print("未获取资源，请重试")

    # 对影片资源进行解析
    print("*" * 80)
    for index,item in enumerate(curl):
        title = item.find('span',class_='s1').get_text()
        type = item.find('p',class_='star').get_text()
        print(index)
        print('类型:' + type)
        print('名称:' + title)
        # print('链接:' + item.get('href'))

        # 获取视频源
        get_video_origin(item.get('href'))


def get_video_origin(url):
    '''
    获取观看Url
    :param url: 视频URL
    :return: 视频链接
    '''

    res = request.urlopen(url)
    html = res.read().decode("UTF-8")

    # print(html)
    # 获取视频源
    soup = BeautifulSoup(html,'html5lib')
    curl = soup.find('div',class_='ji-tab-content').find_all('a')
    yuan = [item.find('span',class_='shipy').get_text() for item in curl]

    # 获取视频标识
    start = html.index("'data':'") + len("'data':'")
    end = html.index("*_*'+vd,")

    identifier = html[start:end]

    # 获取视频源链接
    for yuan_name in yuan:
        # 获取地址
        get_watch_url(yuan_name,identifier)

    # print(yuan)


def get_watch_url(yuan,identifier):
    # url
    url = "http://www.anyunjun.cn/ps.html"
    # 参数
    parms = {
        'data': identifier + '*_*' + yuan,
        't': '{tokens1}'
    }

    # 发起POST请求
    parms_urlencode = bytes(parse.urlencode(parms), encoding=
    'utf8')
    req = request.urlopen(url, data = parms_urlencode)
    html = req.read().decode('UTF-8')
    soup = BeautifulSoup(html,'html5lib')

    curl = soup.find_all('a')
    if len(curl) == 0:
        return

    print("-" * 20 + '播放列表：' + yuan + '-' * 20)
    # 获取播放列表
    for item in curl:
        video_title = item.find('span').get_text()
        video_url = vip_serialize(item.get('href'))
        print('[%s] : %s' % (video_title,video_url))


def vip_serialize(mp4url):
    if 'iqiyi' in mp4url:
        return 'http://vip.jlsprh.com/jiexi/47ks/?url='+mp4url
    elif 'qq' in mp4url:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url
    elif 'sohu' in mp4url:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url
    elif 'youku' in mp4url:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url
    elif 'tudou' in mp4url:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url
    elif 'le' in mp4url:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url
    else:
      return 'http://jx.aeidu.cn/index.php?url='+mp4url


name = input("输入影片名称:\n")
search_film(name)