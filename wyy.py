#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

# 网易云音乐下载

import base64
import binascii
from Crypto.Cipher import AES
# 加密
class RSA(object):
    p_modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pub_key = '010001'

    def __init__(self):
        super().__init__()

    def encrypt(self,text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)[:16]
        enc_text = self.aes_encrypt(self.aes_encrypt(text, self.nonce), sec_key)
        enc_sec_key = self.rsa_encrypt(sec_key, self.pub_key, self.p_modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    def aes_encrypt(self, text, sec_key):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(sec_key, 2, '0102030405060708')
        cipher_text = encryptor.encrypt(text)
        cipher_text = base64.b64encode(cipher_text).decode('utf-8')
        return cipher_text

    def rsa_encrypt(self, text, public_key, p_modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(public_key, 16), int(p_modulus, 16))
        return format(rs, 'x').zfill(256)

    def create_secret_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]

import requests
import json
# api接口
class Api(object):
    headers = {
        'Accept': '*/*',
        'Host': 'music.163.com',
        'User-Agent': 'curl/7.51.0',
        'Referer': 'http://music.163.com',
        'Cookie': 'appver=2.0.2'
    }

    def __init__(self, timeout=30):
        super().__init__()
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.timeout = timeout
    def GET(self, url):
        '''
        GET请求
        :param url: url
        :return: 返回结果
        '''
        response = self.session.get(url, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to get {}'.format(result, url))
        else:
            return result

    def POST(self, url, params):
        '''
        POST请求
        :param url:
        :param params:
        :return:
        '''
        rsa = RSA()
        data = rsa.encrypt(params)
        response = self.session.post(url, data=data, timeout=self.timeout)
        result = response.json()
        if result['code'] != 200:
            print('Return {} when try to post {} => {}'.format(result, params, url))
        else:
            return result

    def parse_data(self,list):
        if len(list) == 0:
            return None
        songs = []
        for item in list:
            # 专辑封面
            albumArt = item['album']['picUrl'] + '?param=400y400'
            # 专辑名称
            albumName = item['album']['name']
            # 歌曲名称
            songName = item['name']
            # 歌手
            songer = item['artists'][0]['name']
            # 歌曲Id
            songId = item['id']

            songInfo = {
                'songName': songName,
                'songer': songer,
                'songId': songId,
                'albumName': albumName,
                'albumArt': albumArt
            }
            songs.append(songInfo)
        return songs

    def get_song_info(self, song_id):
        """
        Get song info by song id
        :param song_id:
        :return:
        """
        url = 'http://music.163.com/api/song/detail/?ids=[%s]' % format(song_id)
        result = self.GET(url)
        list = result['songs']
        return self.parse_data(list)

    def get_album_songs(self, album_id):
        """
        Get all album songs info by album id
        :param album_id:
        :return:
        """
        url = 'http://music.163.com/api/album/%s/' % format(album_id)
        result = self.GET(url)

        list = result['album']['songs']
        return self.parse_data(list)

    def get_song_url(self, song_id, bit_rate=320000):
        """Get a song's download url.
        :params song_id: song id<int>.
        :params bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
        :return:
        """
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        csrf = ''
        params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        result = self.POST(url, params)
        song_url = result['data'][0]['url']
        return song_url

    def get_hot_songs(self, artist_id):
        """
        Get a artist 50 hot songs
        :param artist_id:
        :return:
        """
        url = 'http://music.163.com/api/artist/%s' % format(artist_id)
        print(url)
        result = self.GET(url)
        list = result['hotSongs']
        return self.parse_data(list)

    def get_playlist_songs(self, playlist_id):
        """
        Get a public playlist all songs
        :param playlist_id:
        :return:
        """
        url = 'http://music.163.com/api/playlist/detail?id=%s' % format(playlist_id)
        result = self.GET(url)
        list = result['result']['tracks']
        return self.parse_data(list)

import os
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB, error

# 歌曲信息编辑
class Meta(object):
    def __init__(self):
        super().__init__()


    def read_image(self,url):
        '''
        读取图片url为bytes
        :param url:
        :return:
        '''
        response = requests.get(url)
        data = bytes(response.content)
        return data

    def song_meta(self, path, songInfo):
        '''
        编辑歌曲信息
        :param path:
        :param songInfo:
        :return:
        '''
        try:
            audio = MP3(path, ID3=ID3)
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
        id3 = ID3(path)
        # Remove old 'APIC' frame
        # Because two 'APIC' may exist together with the different description
        # For more information visit: http://mutagen.readthedocs.io/en/latest/user/id3.html
        if id3.getall('APIC'):
            id3.delall('APIC')
        # add album cover
        id3.add(
            APIC(
                encoding=0,  # 3 is for UTF8, but here we use 0 (LATIN1) for 163, orz~~~
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # 3 is for the cover(front) image
                data=self.read_image(songInfo['albumArt'])
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

def downloader(items):
    # 创建下载文件夹
    if not os.path.exists("music"):  # 判断目录是否存在
        os.makedirs("music")  # 创建多级目录

    for item in items:
        songUrl = api.get_song_url(item['songId'])
        if songUrl == None:
            print("\033[1;31;0m【" + item['songName'] + "】无版权" + "，无法下载\033[0m")
        else:
            r = requests.get(songUrl, stream=True)
            file_name = "music/" + item['songName'] + ".mp3"
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            print("\033[1;32;0m【" + item['songName'] + "】 下载完成\033[0m")
            # 编辑歌曲信息
            meta = Meta()
            meta.song_meta(file_name,item)

api = Api()

# 获取歌单列表
songs = api.get_playlist_songs('2235313574')

# 获取专辑列表
# songs = api.get_album_songs('35040037')

# http://music.163.com/#/m/song?id=25706282

# 获取单曲
# songs = api.get_song_info('25657368')

# 获取热门
# songs = api.get_hot_songs('1')

# 下载
downloader(songs)






