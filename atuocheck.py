#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-18 00:30:06
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import time
import xlrd
from xlutils.copy import copy

def autodiscussion (web,list1,list2):
	try:
		web.switch_to.frame("speedgrader_iframe")
	except :
		list1.append("0")
		list2.append("0")
		return
	else:
		list1.append("1")
	text = BeautifulSoup(web.page_source,'lxml')
	answer1=text.find_all("div",class_="discussion_entry communication_message can_be_marked_as_read unread")
	answer2=text.find_all("div",class_="discussion_entry communication_message can_be_marked_as_read read")
	if len(answer1)+len(answer2)==1:
		list2.append("0")
	else:
		list2.append("1")

sectionnumber=[20,21,21]
sectiondoc=["section04.xls","section07.xls","section08.xls"]
sectionweb=["https://uiowa.instructure.com/courses/142906/gradebook/speed_grader?assignment_id=1259715&student_id=165971",
"https://uiowa.instructure.com/courses/142901/gradebook/speed_grader?assignment_id=1259744&student_id=216902",
"https://uiowa.instructure.com/courses/142910/gradebook/speed_grader?assignment_id=1259743&student_id=121706"]


web = webdriver.Chrome()
for j in range(3):
	uiowatest = sectionweb[j]
	web.get(uiowatest)
	time.sleep(3)
	try:
	#log in
		web.find_element_by_id("hawkid").send_keys("jianjyu@uiowa.edu")
		web.find_element_by_id("password").send_keys("yu19940207")
		web.find_element_by_name("uip_action").click()
		#two step varification
		time.sleep(3)
		web.switch_to.frame("duo_iframe")
		web.find_element_by_xpath("//div[@id='auth_methods']/fieldset/div/button").click()
		#please respond within 15s or the programe will shut down
		time.sleep(10)
	except:
		pass
	ns=sectionnumber[j]
	post=["post"]
	conservation=["conservation"]
	for i in range(ns):
		autodiscussion(web, post, conservation)
		#go to the next student
		web.switch_to.parent_frame()
		web.find_element_by_id("next-student-button").click()
		#wait for respond
		time.sleep(2)
	print("finish check")
	print(post,conservation)
	print(sectionnumber[j])


	file = sectiondoc[j]
	file_section = xlrd.open_workbook(filename=file)
	working_file = copy(file_section)
	file_sheet = working_file.get_sheet(0)
	for k in range(ns+1):
		file_sheet.write(k,1,post[k])
		file_sheet.write(k,2,conservation[k])
	working_file.save(sectiondoc[j])
	print("finish input")
	print(sectiondoc[j])


print ("finish")