# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:58 2018
@author: lxcnju
利用selenium模拟登陆爬取王者荣耀官网上的英雄图片和装备图片
"""


from selenium import webdriver          # 模拟登陆
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup           # 页面解析
import re
import time
import os
import requests

chromePath =  r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'         # 谷歌浏览器驱动位置

wd = webdriver.Chrome(executable_path = chromePath)     # 构建浏览器
wait = WebDriverWait(wd, 2)                             # 设定等待时长为100秒

if not os.path.exists("pics"):
    os.mkdir("pics")
if not os.path.exists("pics/small_pics"):
    os.mkdir("pics/small_pics")
if not os.path.exists("pics/equipments_pics"):
    os.mkdir("pics/equipments_pics")

# 下载图片
def download_img(img_url, fpath):
    resp = requests.get(img_url)
    fw = open(fpath, 'wb')
    fw.write(resp.content)
    fw.close()
    print("Save {} to {}...".format(img_url, fpath))
    time.sleep(1)

# 爬取英雄头像    
def crawl_herolist():
    global wd, wait
    # 英雄页
    hero_page_url = "http://pvp.qq.com/web201605/herolist.shtml"
    wd.get(hero_page_url)
    time.sleep(5)
    
    # 获取每个英雄的职位和图片url
    hero_infos = {}
    all_places = ["坦克", "战士", "刺客", "法师", "射手", "辅助"]   # 所有职位
    for i in range(2, 8):
        # 点击按钮
        type_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.wrapper > div > div > div.herolist-box > div.clearfix.herolist-types > ul:nth-child(3) > li:nth-child({})'.format(i)))
        )
        type_btn.click()
        # 源码
        html = wd.page_source
        # 解析该职位下的所有英雄
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.select("body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li")
        for block in blocks:
            img_url = block.select("a > img")[0]["src"]
            hero_name = block.select("a")[0].text.strip()
            print(img_url, hero_name)
            try:
                hero_infos[hero_name]
            except KeyError:
                hero_infos[hero_name] = {"places" : [], "url" : ""}
            hero_infos[hero_name]["places"].append(all_places[i - 2])
            hero_infos[hero_name]["url"] = img_url
    # 下载所有图片
    for hero_name, hero_info in hero_infos.items():
        fname = os.path.join("pics", "small_pics", hero_name + "_" + "_".join(hero_info["places"]) + ".jpg")
        download_img(hero_info["url"], fname)
    print("Done!")

# 爬取所有装备  
def crawl_equipments():
    global wd, wait
    # 装备页
    time.sleep(2)
    item_page_url = "http://pvp.qq.com/web201605/item.shtml"
    wd.get(item_page_url)
    time.sleep(3)
    
    # 获取每个装备的作用和图片url
    items_infos = {}
    all_types = ["攻击", "法术", "防御", "移动", "打野", "辅助"]   # 所有装备类型
    for i in range(2, 8):
        # 点击按钮
        type_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.wrapper > div > div > div.herolist-box > div.clearfix.herolist-types.item-types > ul > li:nth-child({})'.format(i)))
        )
        
        type_btn.click()
        # 源码
        html = wd.page_source
        # 解析该类型下所有装备
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.select("#Jlist-details > li")
        for block in blocks:
            img_url = block.select("a > img")[0]["src"]
            item_name = block.select("a")[0].text.strip()
            if "?" in item_name:
                item_name = "".join(item_name.split("?"))
            if not img_url.startswith("http"):
                img_url = "http:" + img_url
            print(img_url, item_name)
            try:
                items_infos[item_name]
            except KeyError:
                items_infos[item_name] = {"types" : [], "url" : ""}
            items_infos[item_name]["types"].append(all_types[i - 2])
            items_infos[item_name]["url"] = img_url
    # 下载所有图片
    for item_name, item_info in items_infos.items():
        fname = os.path.join("pics", "equipments_pics", item_name + "_" + "_".join(item_info["types"]) + ".jpg")
        download_img(item_info["url"], fname)
    print("Done!")

crawl_herolist()
crawl_equipments()