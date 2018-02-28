#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import os

name = ''


def qq_search(name):
    '''
        搜索腾讯视频
    '''
    url = 'https://v.qq.com/x/search/?q=' + name
    # urlopen不知处中英混合url 需转换
    # 方法quote的参数safe表示可以忽略的字符。
    # string.printable表示ASCII码第33～126号可打印字符，其中第48～57号为0～9十个阿拉伯数字；
    # 65～90号为26个大写英文字母，97～122号为26个小写英文字母，其余的是一些标点符号、运算符号等。
    search_url = quote(url, safe=string.printable)
    res = request.urlopen(search_url)
    html = res.read().decode('UTF-8')
    # print(html)

    soup = BeautifulSoup(html, "html5lib")
    curl = soup.find('h2', class_='result_title').a.get('href')

    if curl:
        return curl
    else:
        print('没有找到该剧的资源!!!!')
        exit(0)


def opencurl(strobj):
    arrycurl = []
    mpHtml = request.urlopen(strobj).read()
    soup = BeautifulSoup(mpHtml, "html5lib")
    curl = soup.find_all('span', class_='item')
    for line in curl:
        if line.a:
            obj = line.a.get('href')
            arrycurl.append(obj)

    print('共找到' + str(len(arrycurl)) + '集')
    cmd = input("\n是否要下载[Y/N]:")  # 等待用户输入
    if cmd == 'Y' or cmd == 'y':
        for index, curl in enumerate(arrycurl):
            download_video(curl, index)  # 开始下载每一集
    else:
        print('no')


def download_video(url, index):
    if not os.path.exists(name):  # 判断目录是否存在
        os.makedirs(name)  # 创建多级目录
    # flag = os.system('python3 /home/pi/Git/you-get/you-get' + ' ' + '-o '+path+ ' ' + strobj )

    print('=' * 80)
    flag = os.system('you-get' + ' ' + '-o ' + name + ' ' + url)
    print('=' * 80)

    if flag != 0:
        print('=========================')
        print('errr' + ' ' + url)
        print('=========================')


# 下载优酷视频
name = input('输入需要下载的电视剧名称:\n')

# 搜索
result_curl = qq_search(name)

opencurl(result_curl)
