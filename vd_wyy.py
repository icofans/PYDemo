#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

# 获取网易云歌单下载

import requests
from bs4 import BeautifulSoup
import os
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB, error
from PIL import Image
from io import BytesIO

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
        # 获取歌曲信息
        infoUrl = 'http://music.163.com/song?id=%s' % item['href'].split('=')[1]
        req = requests.session()
        res = req.get(infoUrl, headers=headers).content
        soup = BeautifulSoup(res, "html5lib")
        cnt = soup.find('div', {'class': 'cnt'})
        cover = soup.find('div', {'class': 'u-cover u-cover-6 f-fl'})

        album = cnt.find_all('a', {'class': 's-fc7'})

        # 专辑封面
        albumArt = cover.find('img').get('data-src')
        # 专辑名称
        albumName = album[-1].string
        # 歌曲名称
        songName = cnt.find('em', {'class': 'f-ff2'}).string
        # 歌手
        songer = album[0].string
        # 歌曲链接
        songUrl = "http://music.163.com/song/media/outer/url?id=%s.mp3" % item['href'].split('=')[1]

        songInfo = {
            'songName': songName,
            'songer': songer,
            'songUrl': songUrl,
            'albumName': albumName,
            'albumArt': albumArt
        }
        songs.append(songInfo)
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
            # 编辑歌曲信息
            edit_song_info(file_name,item)

    print(str(index)+"首歌曲已下载完成")

def read_image(url):
    response = requests.get(url)
    data = bytes(response.content)
    return data

def edit_song_info(file_path,songInfo):
    # If no ID3 tags in mp3 file
    try:
        audio = MP3(file_path, ID3=ID3)
    except HeaderNotFoundError:
        print('Can\'t sync to MPEG frame, not an validate MP3 file!')
        return

    if audio.tags is None:
        print('No ID3 tag, trying to add one!')
        try:
            audio.add_tags()
            audio.save()
        except error as e:
            print('Error occur when add tags:', str(e))
            return

    # Modify ID3 tags
    id3 = ID3(file_path)
    # Remove old 'APIC' frame
    # Because two 'APIC' may exist together with the different description
    # For more information visit: http://mutagen.readthedocs.io/en/latest/user/id3.html
    if id3.getall('APIC'):
        id3.delall('APIC')
    # add album cover
    id3.add(
        APIC(
            encoding=0,         # 3 is for UTF8, but here we use 0 (LATIN1) for 163, orz~~~
            mime='image/jpeg',  # image/jpeg or image/png
            type=3,             # 3 is for the cover(front) image
            data=read_image(songInfo['albumArt'])
        )
    )
    # add artist name
    id3.add(
        TPE1(
            encoding=3,
            text=songInfo['songer']
        )
    )
    # add song name
    id3.add(
        TIT2(
            encoding=3,
            text=songInfo['songName']
        )
    )
    # add album name
    id3.add(
        TALB(
            encoding=3,
            text=songInfo['albumName']
        )
    )
    id3.save(v2_version=3)


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



