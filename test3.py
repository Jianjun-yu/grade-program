#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-03 00:15:07
# @Author  : Qianmu (jianjyu@uiowa.edu)
# @Link    : not yet
# @Version : $Id$

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import time
web = webdriver.Chrome()
uiowatest = "https://uiowa.instructure.com/courses/145951/gradebook/speed_grader?assignment_id=1238578&student_id=235595"
web.get(uiowatest)
time.sleep(3)
#log in
web.find_element_by_id("hawkid").send_keys("jianjyu@uiowa.edu")
web.find_element_by_id("password").send_keys("yu19940207")
web.find_element_by_name("uip_action").click()
#two step varification
time.sleep(120)
web.switch_to.frame("duo_iframe")
web.find_element_by_xpath("//div[@id='auth_methods']/fieldset/div/button").click()
#please respond within 15s or the programe will shut down
time.sleep(10)
print("time")
a = web.find_element_by_id("grading-box-extended").get_attribute('value')
print(len(a))
print (type(a))
print(a)
print ("finish")