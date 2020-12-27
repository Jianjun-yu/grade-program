#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-01 22:24:44
# @Author  : Qianmu (jianjyu@uiowa.edu)
# @Link    : not yet
# @Version : $Id$

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from bs4 import BeautifulSoup
import copy
import os
#利用网页地址变化检查网页是否跳转,注意输入oldweb_url的时候要使用深复制获取老的url的复制而不是引用。
def loading_success_check1(oldweb_url,newweb_url,star = None,end = None):
	i = 0 
	while newweb_url[star:end] == oldweb_url[star:end]:
		time.sleep(5)
		i += 1
		if i == 12:
			print ("Loading failure")
			return False
	return True

#利用网站内容检查网页是否跳转，似乎没啥必要还，留一个位置先
#通用性更强，在知道将要跳转的网站特征以及将要跳转的网站与与原网站的明显区别的时候，非常有效
def loading_success_check2(key,web):
	
	pass


#登录特定网站,全校通用，除非学校改了登录网站的结构.....
def login(url = "https://uiowa.instructure.com/courses/115342/files/10003643?module_item_id=2956932", id = "jianjyu@uiowa.edu" , password = "yu19600905"):
	#打开浏览器，讲道理其实有效率更高的方法的，不过比较懒也不差这点效率了，问题不大
	web = webdriver.Chrome()
	#打开指定网页
	weburl = url
	web.get(weburl)
	#等待网页加载，至少一秒，一般应该5-10秒，取决于网速
	time.sleep(1)
	#登录hawkid账号
	web.find_element_by_id("hawkid").send_keys(id)
	web.find_element_by_id("password").send_keys(password)
	web.find_element_by_name("uip_action").click()
	if loading_success_check1(url,web.page_source):
		return web
	else:
		print ( "Loading failure, please check internet, account, and password" )
		return 

#通过手机二次验证，感觉安全性还挺高的，懒得读取了直接模拟鼠标反正也不差这点效率，问题不大，
#不过万一程序运行的时候有人动了鼠标怎么办....虽然只有不到1秒的鼠标限制....
def duo_check1(web):
	#记录一下原来的网站信息
	oldweb = copy.copy(web.current_url)
	#确定鼠标起始点
	mouse = web.find_element_by_link_text("More Information on Two-Step Login")
	#启动鼠标模拟
	action = ActionChains(web)
	#确定向目标方向移动距离即后续操作，执行上述所有行动
	action.move_to_element_with_offset(mouse,300,-435).click().perform()
	#等待手机响应完成二次验证，然后等待网页加载
	#检测网页是否跳转
	if loading_success_check1(oldweb,web.current_url):
		return web
	else:
		print ("failed to duo_check, 10 seconds to exit")
		os._exit(10)
#一个更稳健的执行二次验证的方式
def duo_check2(web):
	pass

def gettext(web,path_iframe = "//*[@id='doc_preview']/div/iframe",check_class="textLayer--absolute"):
	#建立一个空的list存文本
	textlist = []
	#加载进入文本框
	web.switch_to.frame(web.find_element_by_xpath(path_iframe))
	#等待文本加载，使用内置方法检查,以textLayer--absolute为检查点，检查是否加载完成
	#两秒后开始检查
	wait = WebDriverWait(web,2)
	#每500毫秒轮检一次，其实还不如sleep效率高，但是稳的一批，谁知道网络会出什么鬼
	wait.until(expected_conditions.element_to_be_selected((By.CLASS_NAME , check_class)))
	#加载过滤模块，注意，要配置lxml环境，或者使用python内置方法，不过忘记python内置方法是什么了....
	text = BeautifulSoup(web.page_source,'lxml')
	#定位文本位置，读取全部含文本元素，这个地方之前要补一个检测未提交的方法，然后用try函数加强
	allcontent = text.find_all(class_=check_class)
	#通过循环，依次抽取含文本元素
	for eachsentence in allcontent:
		#将元素中的文本取出
		#去除空格
		sentence = eachsentence.getText().strip()
		#加入列表中保证
		textlist.append(sentence)
	return textlist
def check_empty(web):
	pass

def check_keys_1 (textlist,keys=[]):
	points = 0
	for i in keys:
		str(i.strip())
		for j in textlist:
			if i == j:
				points +=1
	return points
def check_key_2(textlist,keys=[]):
	pass
def input(web, points, comments):
	pass
def next_student(web):
	pass
def check_name(web = uiowaweb, grades = name_grade_tuple ):
	grades_value = 0
	text = BeautifulSoup(web.page_source,'lxml')
	postion_name = text.find(class_= "ui-selectmenu-item-header")
	name = postion_name.getText().strip()
	first_name = name.split(" ",1)[0].strip()
	last_name =name.split(" ",1)[1].strip()
	fuzzy_ratio_last_name = 0
	fuzzy_ratio_first_name = 0
	for i in grades:
		if  fuzz.ratio(last_name, grades(i)[0].strip())==100:
			if fuzz.ratio(first_name,grades(i)[1])==100:
				grades_value = grades(i)[2]
				break
			else:
				if fuzz.ratio(first_name,grades(i)[1].strip()) > fuzzy_ratio_first_name:
					fuzzy_ratio_first_name = fuzz.ratio(first_name,grades(i)[1])
					grades_value = grades(i)[2]
		else:
			if fuzz.ratio(last_name,grades(i)[1].strip()) > fuzzy_ratio_last_name:
				fuzzy_ratio_last_name = fuzz.ratio(last_name,grades(i)[1].strip())
				if fuzz.ratio(first_name,grades(i)[1])==100:
					grades_value = grades(i)[2]
				else:
					if fuzz.ratio(first_name,grades(i)[1].strip()) > fuzzy_ratio_first_name:
						fuzzy_ratio_first_name = fuzz.ratio(first_name,grades(i)[1])
						grades_value = grades(i)[2]