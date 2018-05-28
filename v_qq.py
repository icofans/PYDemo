#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

import requests
from requests.exceptions import RequestException
import re
import json

headers={
    'Accept-Encoding':'identity;q=1, *;q=0',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Accept':'*/*',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

#这一部分是为了得到网页源代码
def get_html(url):
    response=requests.get(url,headers=headers)
    try:
        if  response.status_code==200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None

#这一部分是为了得到参数vid
def parse_part_1(url):
    try:
        vid=url.split('/')[-1].split('.')[0]
        print('解析URL第一部分vid:'+vid)
        return vid
    except Exception:
        print('解析vid失败')

#这一部分是为了得到keyid、vkey、title、pre_url
def parse_part_2(html):
    try:
        pattern=re.compile('JsonpCallBack\((.*)\)',re.S)
        data=re.search(pattern,html).group(1)
        data=json.loads(data)
        keyid=data.get('vl').get('vi')[0].get('cl').get('ci')[0].get('keyid')
        if len(keyid.split('.'))==3:
            if '10' in keyid:
                keyid=keyid.replace('10', 'p')
            else:
                keyid=list(keyid)
                keyid[12]='p'
                keyid=''.join(keyid)
        else:
            keyid=keyid
        print('解析URL第二部分keyid:'+keyid)
        vkey=data.get('vl').get('vi')[0].get('fvkey')
        print('解析URL第二部分vkey:'+vkey)
        title=data.get('vl').get('vi')[0].get('ti')
        # print('解析URL第二部分title:' + title)
        for i in range(4):
            pre_url=data.get('vl').get('vi')[0].get('ul').get('ui')[i].get('url')
            print('解析URL第二部分pre_url:'+pre_url)
            yield {
                'keyid':keyid,
                'pre_url':pre_url,
                'vkey':vkey,
                'ti':title
                   }
    except Exception:
        print('解析vkey失败')

#主程序
def main(url):
    try:
        vid=parse_part_1(url)
        if vid:
            url='https://av.video.qq.com/getinfo?callback=JsonpCallBack&&charge=0&defaultfmt=auto&otype=json&guid=c05f836b267c173e684cec6410185d3b&platform=70201&sdtfrom=v1104&defnpayver=0&appVer=3.3.128&host=v.qq.com&ehost=https%3A%2F%2Fv.qq.com%2F&_rnd=1507969615&spwm=4&vid={}&_qv_rmt=ZHrqJgF6A10991DBb%3D&_qv_rmt2=y%2FlweBl0157665zsQ%3D&_1507969615506='.format(vid)
            html=get_html(url)
            if html:
                for each in parse_part_2(html):
                    keyid=each.get('keyid')
                    pre_url=each.get('pre_url')
                    vkey=each.get('vkey')
                    title=each.get('ti')
                    url=pre_url+str(keyid)+'.mp4?vkey='+str(vkey)
                    print('=====视频:{0}=====下载URL:{1}'.format(title,url)+'\n')
    except Exception:
        print('解析视频下载URL失败')

if __name__=='__main__':
    main('https://v.qq.com/x/page/j002109hlhs.html')