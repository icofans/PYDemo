#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

import requests
import xlwt

def getProvince(provinceNum):
    '''
    获取省份
    :param provinceNum: 省份id
    :return: 返回省份名称
    '''
    pronvince = ''
    switcher = {
        "100": "北京",
        "200": "广东",
        "210": "上海",
        "220": "天津",
        "230": "重庆",
        "240": "辽宁",
        "250": "江苏",
        "270": "湖北",
        "280": "四川",
        "290": "陕西",
        "311": "河北",
        "351": "山西",
        "371": "河南",
        "431": "吉林",
        "451": "黑龙江",
        "471": "内蒙古",
        "531": "山东",
        "551": "安徽",
        "571": "浙江",
        "591": "福建",
        "731": "湖南",
        "771": "广西",
        "791": "江西",
        "851": "贵州",
        "871": "云南",
        "891": "西藏",
        "898": "海南",
        "931": "甘肃",
        "951": "宁夏",
        "971": "青海",
        "991": "新疆"
    }
    return switcher.get(provinceNum, "")

def getProductList(productId,row):
    '''
    获取套餐列表
    :param productId:
    :return:
    '''
    params = {'productId': str(productId)}
    res = requests.get("http://wx.10086.cn/website/businessPlatform/shopList/data", params=params)
    response = res.json()

    col = 0
    if response.get("code") == "A00006":
        # 获取套餐档位
        norms = response.get('norms')

        # 打印套餐信息
        print("-"*40 +  str(productId) + "-"*40)
        print("套餐省份: %s" % getProvince(response.get("province")))
        print("套餐名称: %s [%s]" % (response.get("productname"),response.get("intro")))

        price = ""
        for index,item in enumerate(norms):
            price =  item.get("name") + "( ¥ " + item.get("price") + ")"+ '\n' + price
            print("套餐价格: %s - %s" % (item.get("name"),item.get("price")))
        print("办理地址: %s" % response.get("weburl"))
        print("-"*90)

        # 写入表格
        booksheet.write(row,col,str(row)) # 套餐代码
        col = col + 1
        booksheet.write(row,col,str(productId)) # 套餐代码
        col = col + 1
        booksheet.write(row,col,response.get("province")) # 套餐省份代码
        col = col + 1
        booksheet.write(row,col,getProvince(response.get("province"))) # 套餐省份
        col = col + 1
        booksheet.write(row,col,response.get("productname")) # 套餐名称
        col = col + 1
        booksheet.write(row,col,response.get("intro")) # 套餐简介
        col = col + 1
        booksheet.write(row,col,price) # 套餐价格
        col = col + 1
        booksheet.write(row,col,response.get("weburl")) # 办理地址

        # ++
        global bookRow
        bookRow = row + 1


# 创建表格
workbook=xlwt.Workbook(encoding='utf-8')
booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

# 表格标题栏
booksheet.write(0, 0, "序号")
booksheet.write(0, 1, "套餐代码")
booksheet.write(0, 2, "套餐省份编码")
booksheet.write(0, 3, "套餐省份")
booksheet.write(0, 4, "套餐名称")
booksheet.write(0, 5, "套餐简介")
booksheet.write(0, 6, "套餐价格")
booksheet.write(0, 7, "办理地址")


# 创建表格索引
bookRow = 1

for i in range(100,999):
    getProductList(i,bookRow)

# 表格存储
workbook.save('grade.xls')