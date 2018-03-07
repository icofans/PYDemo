#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

'''
获取全民影院热门推荐
'''

from urllib import request
from bs4 import BeautifulSoup
from urllib import parse
import http.client
import util

def get_hot_video():
    url = "http://www.anyunjun.cn"
    res = request.urlopen(url)
    html = res.read().decode("UTF-8")

    soup = BeautifulSoup(html,'html5lib')
    curl = soup.find_all('div',class_='b-listtab-main')

    for index,item in enumerate(curl):
        # 热门影片
        if index == 0:
            print('【热门影片】')
            get_video_list(item)
        elif index == 1:
            print('\n\n【热门电视剧】')
            get_video_list(item)


def get_video_list(item):

    items = item.find_all('a',class_='js-tongjic')
    for index,video in enumerate(items):
        title = video.find('span',class_='s1').get_text()
        # protagonist = video.find('p',class_='star').get_text()
        url = video.get('href')

        print('\n%s %s' % (index+1,title))
        # print('主演 %s' % protagonist)

        get_video_origin(url)

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

    # 获取播放列表
    for item in curl:
        video_title = item.find('span').get_text()
        video_url = vip_serialize(item.get('href'))
        short_url = util.get_short_url(video_url)
        video_title = video_title.replace(' ','')
        video_title = video_title.replace('\n','')
        print('[%s] [%s] : %s' % (yuan,video_title,short_url))


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



def get_short_url(url):
    conn = http.client.HTTPConnection('suo.im')
    params = parse.urlencode({'format':'json','url': url})
    conn.request('POST', '/api.php', headers={"Content-Type": "application/x-www-form-urlencoded"}, body=params)
    result = conn.getresponse()
    resultContent = result.read().decode('UTF-8')
    if len(resultContent):
        return resultContent
    else:
        return url


get_hot_video()
