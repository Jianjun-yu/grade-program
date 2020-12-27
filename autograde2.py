#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-12 16:41:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

uiowaweb = webdriver.Chrome()
#open speedgrade websit
uiowatest = "https://uiowa.instructure.com/courses/115342/gradebook/speed_grader?assignment_id=939179&student_id=97493"
uiowaweb.get(uiowatest)
#wait for website respond
time.sleep(5)
#log in 
uiowaweb.find_element_by_id("hawkid").send_keys("jianjyu@uiowa.edu")
uiowaweb.find_element_by_id("password").send_keys("yu19600905")
uiowaweb.find_element_by_name("uip_action").click()
#two step varification
mouse = uiowaweb.find_element_by_link_text("More Information on Two-Step Login")
action = ActionChains(uiowaweb)
#the the button to begin two varification
action.move_to_element_with_offset(mouse,300,-435).click().perform()
#please respond within 15s or the programe will shut down
time.sleep(15)

for i in range(242):
	#input the grade
	#go to the next student
	try :
		uiowaweb.switch_to.frame("speedgrader_iframe")
	except Exception:
		grades_value = 0
		uiowaweb.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
	else:
		grades_value = 0.3
		uiowaweb.switch_to.parent_frame()
		uiowaweb.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
	uiowaweb.find_element_by_id("comment_submit_button").click()
	uiowaweb.find_element_by_id("next-student-button").click()
	#wait for respond
	time.sleep(3)

print("finish")


