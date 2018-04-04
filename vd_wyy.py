#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

# 获取网易云歌单下载

import requests
import urllib
from bs4 import BeautifulSoup

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
    return songs

# 下载歌曲
def dowload_mp3(items):
    for item in items:
        print(item['songName']+'开始下载.....')
        try:
            urllib.request.urlretrieve(item['songUrl'], item['songName'] + '.mp3')
        except:
            x = x - 1
            print('下载出错')


songs = get_play_list("103514604")
dowload_mp3(songs)