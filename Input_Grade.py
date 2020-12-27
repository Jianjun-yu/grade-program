#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-10-23 12:47:03
# @Author  : Qianmu (jianjyu@uiowa.edu)
# @Link    : not yet
# @Version : $Id$

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from difflib import SequenceMatcher
import time
from bs4 import BeautifulSoup
import sys
import os
import xlrd


def input_grade(web, grades):
	#read the websit
	text = BeautifulSoup(web.page_source,'lxml')
	#find the name of student
	postion_name = text.find(class_= "ui-selectmenu-item-header")
	#pick the name
	name = postion_name.getText().strip()
	first_name = name.split(" ", 1)[0].strip()
	last_name = name.split(" ", 1)[1].strip()
	#initiate the grade
	current_grade = web.find_element_by_id("grading-box-extended").get_attribute('value')
	if len(current_grade)!=0:
		print(current_grade)
		return
	else:
		pass
	grades_value = 120
	#find the grade in the excel. match with each row of the excel
	for i in range(grades.nrows):
		#match the last name
		#if last_name == grades.row_values(i)[2].strip():
		#if the student's name are provided in one col
		if last_name == grades.row_values(i)[0].strip().split(",", 1)[0].strip():
			#if last name is matched, try to match first name
			#if first_name == grades.row_values(i)[3].strip():
			#if in the spreadsheet, the student's name are provided in one col
			if  first_name == grades.row_values(i)[0].strip().split(",", 1)[1].strip():
				#if both names are matched, pick the grade
				grades_value = grades.row_values(i)[2]
				#input extra creditb
				#grades_value = 0.2
				#input the grade to icon
				web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
				#web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
				#jump out of the loop
				break
	# if no name in the excel matches with the student, try to find the most similar one
	if grades_value == 120:
		#consider the first name and the last name together
		fullname = first_name+last_name
		#degree of similarity
		degree_of_similarity = 0
		#caculate the degree of similarity in each row 
		for j in range(grades.nrows):
			#get the name in the excel
			# exl_first_name = grades.row_values(i)[3].strip()
			# exl_last_name = grades.row_values(i)[2].strip()
			# exl_fullname = grades.row_values(i)[3].strip() + grades.row_values(i)[2]
			exl_first_name = grades.row_values(j)[0].strip().split(",", 1)[1].strip()
			exl_last_name = grades.row_values(j)[0].strip().split(",", 1)[0].strip()
			exl_fullname = exl_first_name+exl_last_name
			#caculate the degree of similarity
			similarity = SequenceMatcher(None, fullname, exl_fullname).ratio()
			#find the most similar one
			if similarity > degree_of_similarity:
				#defun if input extra credit
				grades_value = grades.row_values(j)[1]
				grade_first_name = exl_first_name
				grade_last_name = exl_last_name
				degree_of_similarity = similarity
		#input the grade of the most similar one 
		#web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
		#input extra credit
		if degree_of_similarity > 0.8:
			#web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
			print (first_name + last_name)
			print ("guess")
			print ( grade_first_name + grade_last_name )
			print ("grade")
			print (str(grades_value))
			print (degree_of_similarity)
			print (" ")
		else:
			print (first_name + last_name)
			print ("guess")
			print (grades_value)
			print ( grade_first_name + grade_last_name )
			print ("no grade find")
			print (degree_of_similarity)
			print ("")
			#grades_value = 0.2
		#else:
		#	grades_value = 0
		
		
	return

file = "introcp.xlsx"
file_grades = xlrd.open_workbook(filename=file)
file_sheet = file_grades.sheet_by_index(0)
name_grade_tuple = file_sheet.row_values
uiowaweb = webdriver.Chrome()
#open speedgrade websit
uiowatest = "https://uiowa.instructure.com/courses/145951/gradebook/speed_grader?assignment_id=1238594&student_id=181522"
uiowaweb.get(uiowatest)
#wait for website respond
time.sleep(10)
#log in
uiowaweb.find_element_by_id("hawkid").send_keys("jianjyu@uiowa.edu")
uiowaweb.find_element_by_id("password").send_keys("yu19940207")
uiowaweb.find_element_by_name("uip_action").click()
#two step varification
time.sleep(3)
uiowaweb.switch_to.frame("duo_iframe")
uiowaweb.find_element_by_xpath("//div[@id='auth_methods']/fieldset/div/button").click()
#please respond within 15s or the programe will shut down
time.sleep(10)
#the number of student you need to grade
for i in range(153):
	#input the grade
	input_grade(uiowaweb, file_sheet)
	#go to the next student
	time.sleep(1)
	uiowaweb.find_element_by_id("comment_submit_button").click()
	time.sleep(0.5)
	uiowaweb.find_element_by_id("next-student-button").click()
	#wait for respond
	time.sleep(1)
print("finish")
