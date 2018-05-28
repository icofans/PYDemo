#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

'''
使用you-get工具下载芒果TV剧集
'''

from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import os


def download_mg_video(name):
	url = 'https://so.mgtv.com/so/k-' + name
	# urlopen不知处中英混合url 需转换
	# 方法quote的参数safe表示可以忽略的字符。
	# string.printable表示ASCII码第33～126号可打印字符，其中第48～57号为0～9十个阿拉伯数字；
	# 65～90号为26个大写英文字母，97～122号为26个小写英文字母，其余的是一些标点符号、运算符号等。
	search_url = quote(url,safe=string.printable)
	res = request.urlopen(search_url)
	html = res.read().decode('UTF-8')

	soup = BeautifulSoup(html,"html5lib")
	curl = soup.find('div',class_='searchresult-foldup').find_all('a')


	arrycurl = []
	# 获取剧集-最后一项是收起 需要过滤
	for index,item in enumerate(curl[:-1]):
		href =  'http:' + item.get('href')
		arrycurl.append(href)

	print('共找到'+str(len(arrycurl))+'集')
	cmd  = input("\n是否要下载[Y/N]:\n") #等待用户输入
	if cmd=='Y' or cmd == 'y' :
		for index,curl in enumerate(arrycurl):
			you_get_download(curl,index) #开始下载每一集
	else:
		for index,curl in enumerate(arrycurl):
			you_get_watch_url(curl,index) #开始下载每一集

def you_get_download(url,index):
	if not os.path.exists(name): # 判断目录是否存在
		os.makedirs(name)  # 创建多级目录

	filename = name+'第'+str(index+1)+'集'

	print('%s:%s' % (filename,vip_serialize(url)))
	flag = os.system('you-get' + ' ' + '-o ' + name + ' ' + '-O ' + filename + ' ' + url )

	if flag != 0:
		print('=========================')
		print('errr' +' ' + url)
		print('=========================')


def you_get_watch_url(url,index):
	filename = name + '第' + str(index + 1) + '集'
	print('%s:%s' % (filename, vip_serialize(url)))


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

def user_tip():
	print("*" * 80)
	print('''
	芒果TV剧集下载：
	1. 需要用到的依赖模块有bs4，html5lib，you-get, 使用pip3 install xxx 安装相应依赖库
	2. 需要输入名称精确搜索
	''')
	print("*" * 80 + '\n')

user_tip()
name = input('输入需要下载的电视剧名称:\n')
# 搜索下载
download_mg_video(name)
