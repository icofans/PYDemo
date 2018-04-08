#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

# 获取网易云歌单下载

import requests
import urllib
from bs4 import BeautifulSoup
import os

# 获取歌单歌曲列表
def get_play_list(id):
    headers = {
        'Referer': 'http://music.163.com/',
        'Host': 'music.163.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = "http://music.163.com/playlist?id="+id
    request = requests.session()
    response = request.get(url,headers=headers).content
    soup = BeautifulSoup(response,"html5lib")
    res = soup.find('ul',{'class':'f-hide'})

    # 获取歌曲下载地址
    arr = res.find_all('a')
    songs = []
    for item in arr:
        songName = item.text
        songUrl = "http://music.163.com/song/media/outer/url?id=%s.mp3" % item['href'].split('=')[1]
        songs.append({'songName':songName,'songUrl':songUrl})
    print(songs)
    return songs

def download_mp3(items):
    '''
    下载mp3
    :param items: 需要下载的文件集合
    :return:
    '''
    # 创建下载文件夹
    if not os.path.exists("music"):  # 判断目录是否存在
        os.makedirs("music")  # 创建多级目录

    index = 0
    for item in items:
        print("开始下载 " + item['songName'])
        r = requests.get(item['songUrl'],stream=True)
        if r.url == "http://music.163.com/404":
            print("    \033[1;31;0m【"+ item['songName'] +"】无版权"+"，无法下载\033[0m")
        else:
            index = index + 1
            file_name = "music/"+item['songName']+".mp3"
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print("    \033[1;32;0m【" + item['songName'] + "】下载完成\033[0m")

    print(str(index)+"首歌曲已下载完成")


def user_tip():
	print("*" * 80)
	print('''
	输入网易云歌单Id以获取
	如： http://music.163.com/playlist?id=xxxxx  【xxxxx】 即为歌单Id 输入 xxxxx 回车
	''')
	print("*" * 80 + '\n')

user_tip()
name = input('输入网易云歌单Id:\n')


songs = get_play_list(name)
download_mp3(songs)


