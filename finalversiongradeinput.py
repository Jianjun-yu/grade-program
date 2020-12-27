#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-25 14:00:34
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from selenium import webdriver
from difflib import SequenceMatcher
import time
from bs4 import BeautifulSoup
import sys
import os
import xlrd

class InputGrade:

	def __init__(self,website,grade_file):
		self.file = xlrd.open_workbook(filename=grade_file)
		self.web = webdriver.Chrome()
		self.web.get(website)
	
	def login_student (self,account,password):
		if len(account) == 0:
			time.sleep(60)
		else:
			time.sleep(5)
			self.web.find_element_by_id("hawkid").send_keys(account)
			self.web.find_element_by_id("password").send_keys(password)
			self.web.find_element_by_name("uip_action").click()
			time.sleep(3)
			self.web.switch_to.frame("duo_iframe")
			self.web.find_element_by_xpath("//div[@id='auth_methods']/fieldset/div/button").click()
			time.sleep(30)

	def read_web_name (self):
		text = BeautifulSoup(self.web.page_source,'lxml')
		#find the name of student
		postion_name = text.find(class_= "ui-selectmenu-item-header")
		#pick the name
		name = postion_name.getText().strip()
		first_name = name.split(" ",1)[0].strip()
		last_name =name.split(" ",1)[1].strip()
		full_name =first_name + last_name
		return full_name

	def all_grade(self,sheet,row1,row2,type,col1,col2,col_grade):
		grade_sheet = self.file.sheet_by_index(sheet-1)
		grade_dict = {}
		if type == True:
			for i in range(row1-1,row2):
				the_row = grade_sheet.row_values(i)
				name = self.read_excel_name1(the_row,col1-1,col2)
				grade = self.read_grade(the_row,col_grade-1)
				grade_dict[name] = grade
		else:
			for i in range(row1-1,row2):
				the_row = grade_sheet.row_values(i)
				name = self.read_excel_name2(the_row,col1-1,col2-1)
				grade = self.read_grade(the_row,col_grade-1)
				grade_dict[name] = grade 
		return grade_dict

	def read_excel_name1 (self,row,col1,col2):
		if col2 == True:
			last_name = row[col1].strip().split(",",1)[0].strip()
			first_name = row[col1].strip().split(",",1)[1].strip()
			full_name = first_name + last_name
		else :
			last_name = row[col1].strip().split(",",1)[1].strip()
			first_name = row[col1].strip().split(",",1)[0].strip()
			full_name = first_name + last_name
		return full_name

	def read_excel_name2(self,row,col1,col2):
		last_name = row[col1].strip()
		first_name = row[col2].strip()
		full_name = first_name + last_name
		return full_name

	def read_grade (self,row,col):
		grade = row[col]
		return grade

	def match_grade(self,name,grade_dict):
		try:
			grade = grade_dict[name]
		except KeyError:
			vagueness = self.vague_match(name,grade_dict)
			vague_name = vagueness[0]
			vague_grade = vagueness[1]
			similarity = vagueness[2]
			return [vague_name,vague_grade,similarity]
		else:
			return grade

	def vague_match(self,name,grade_dict):
		degree_of_similarity = 0
		for i in grade_dict:
			similarity = SequenceMatcher(None,name,i).ratio()
			if similarity > degree_of_similarity:
				vague_name = i
				vague_grade = grade_dict[i]
				degree_of_similarity = similarity
			else:
				pass
		return [vague_name,vague_grade,degree_of_similarity]

	def input_grade(self,grade):
		if type(grade) !=list:
			self.web.find_element_by_id("grading-box-extended").send_keys(str(grade))
		else :
			if grade[2]>=0.7:
				self.web.find_element_by_id("grading-box-extended").send_keys(str(grade[1]))

	def write(self,name,grade):
		f = open("vague_match.txt","a")
		f.write("\nStudent Name")
		f.write("\n")
		f.write(name)
		f.write("\nGuess Name")
		f.write("\n")
		f.write(grade[0])
		f.write("\nGrade")
		f.write("\n")
		f.write(str(grade[1]))
		f.write("\nSimmilarity")
		f.write("\n")
		f.write(str(grade[2]))
		f.write("\n")
		f.close()

	def students(self,account,password,sheet,col1,col2,col_grade,way,row1,row2,number):
		self.login_student(account,password)
		grade_dict = self.all_grade(sheet,row1,row2,way,col1,col2,col_grade)
		for i in range(number):
			student_name = self.read_web_name()
			grade = self.match_grade(student_name,grade_dict)
			self.input_grade(grade)
			if type(grade) == list:
				self.write(student_name,grade)
			else:
				pass
			#self.web.find_element_by_id("comment_submit_button").click()
			self.web.find_element_by_id("next-student-button").click()
			time.sleep(1.5)
		print ("finish")

	def Stop(self):
		os._exit() 
		