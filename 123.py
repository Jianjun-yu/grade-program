#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-28 11:50:31
# @Author  : Qianmu Yu
# @Link    : 111
# @Version : 2.0

from selenium import webdriver
from difflib import SequenceMatcher
import time
from bs4 import BeautifulSoup
import sys
import os
import xlrd
import wx
import threading

class InputGrade:

	def __init__(self,website,grade_file):
		if grade_file == 1:
			pass
		else:
			self.file = xlrd.open_workbook(filename=grade_file)
		self.web = webdriver.Chrome()
		self.web.get(website)
		self.exist = 0
	
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
			pass
			self.web.find_element_by_id("grading-box-extended").send_keys(str(grade))
		else :
			if grade[2]>=0.7:
				pass
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
			if self.exist == 0:
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
			else:
				print ("Stop")
				return
		print ("finish")

	def auto_check(self,account,password,grade1,grade2,number):
		self.login_student(account,password)
		for i in range(number):
			if self.exist == 0:
		#input the grade
		#go to the next student
				try :
					self.web.switch_to.frame("speedgrader_iframe")
				except Exception:
					grades_value = grade1
					self.web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
				else:
					grades_value = grade2
					self.web.switch_to.parent_frame()
					self.web.find_element_by_id("grading-box-extended").send_keys(str(grades_value))
				self.web.find_element_by_id("comment_submit_button").click()
				self.web.find_element_by_id("next-student-button").click()
				#wait for respond
				time.sleep(3)
			else:
				print("stop")

	def Stop(self):
		self.exist = 1

class Grade_GUI(wx.App):
	def OnInit(self):
		frame = wx.Frame(parent=None,title="Input Students' Grade",size=(800,500))
		panel = wx.Panel(frame,-1)
		font1 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
		button1 = wx.Button(panel,-1,"Input Grade",(100,380))
		button2 = wx.Button(panel,-1,"Stop",(500,380))
		button3 = wx.Button(panel,-1,"Auto Check",(300,380))

		label1 = wx.StaticText(panel,-1,"SpeedGrade Website",pos=(10,10))
		label1.SetFont(font1)
		text1 = wx.TextCtrl(panel,-1,pos=(200,10),size=(400,20))

		label2 = wx.StaticText(panel,-1,"Grade Book",pos=(10,35))
		label2.SetFont(font1)
		text2 = wx.TextCtrl(panel,-1,pos=(200,35),size=(150,20))

		radio3_1 = wx.RadioButton(panel, -1, "Student", pos=(10, 60),size=(80,30))
		radio3_1.SetFont(font1)
		radio3_2 = wx.RadioButton(panel, -1, "Teacher", pos=(150, 60),size=(80,30))
		radio3_2.SetFont(font1)

		label4 = wx.StaticText(panel,-1,"Account",pos=(10,90))
		label4.SetFont(font1)
		label4.Enable(False)
		text4 = wx.TextCtrl(panel,-1,pos=(10,115),size=(250,20))
		text4.Enable(False)

		label5 = wx.StaticText(panel,-1,"Password",pos=(300,90))
		label5.SetFont(font1)
		label5.Enable(False)
		text5 = wx.TextCtrl(panel,-1,pos=(300,115),size=(250,20))
		text5.Enable(False)

		label6 = wx.StaticText(panel,-1,"Number of Students",pos=(10,140))
		label6.SetFont(font1)
		text6 = wx.TextCtrl(panel,-1,pos=(200,140),size=(50,20))

		label7 = wx.StaticText(panel,-1,"Sheet of Grade",pos=(10,165))
		label7.SetFont(font1)
		text7 = wx.TextCtrl(panel,-1,pos=(200,165),size=(50,20))

		label8 = wx.StaticText(panel,-1,"Begining Row",pos=(10,190))
		label8.SetFont(font1)
		text8 = wx.TextCtrl(panel,-1,pos=(200,190),size=(50,20))

		label9 = wx.StaticText(panel,-1,"End Row",pos=(10,215))
		label9.SetFont(font1)
		text9 = wx.TextCtrl(panel,-1,pos=(200,215),size=(50,20))

		radio10_1 = wx.RadioButton(panel, -1, "Name in two Column", pos=(10, 240),size=(250,30),style=wx.RB_GROUP)
		radio10_1.SetFont(font1)
		radio10_2 = wx.RadioButton(panel, -1, "Name in one Column", pos=(300, 240),size=(300,30))
		radio10_2.SetFont(font1)

		label11 = wx.StaticText(panel,-1,"Column of First Name",pos=(10,270))
		label11.SetFont(font1)
		label11.Enable(False)
		text11 = wx.TextCtrl(panel,-1,pos=(200,270),size=(50,20))
		text11.Enable(False)

		label12 = wx.StaticText(panel,-1,"Column of Last Name",pos=(10,295))
		label12.SetFont(font1)
		label12.Enable(False)
		text12 = wx.TextCtrl(panel,-1,pos=(200,295),size=(50,20))
		text12.Enable(False)

		label13 = wx.StaticText(panel,-1,"Column of Name",pos=(300,270))
		label13.SetFont(font1)
		label13.Enable(False)
		text13 = wx.TextCtrl(panel,-1,pos=(450,270),size=(50,20))
		text13.Enable(False)

		radio14_1 = wx.RadioButton(panel, -1, "First Name First", pos=(300, 295),size=(200,30),style=wx.RB_GROUP)
		radio14_1.SetFont(font1)
		radio14_1.Enable(False)
		radio14_2 = wx.RadioButton(panel, -1, "Last Name First", pos=(500, 295),size=(200,30))
		radio14_2.SetFont(font1)
		radio14_2.Enable(False)

		label15 = wx.StaticText(panel,-1,"Column of Grade",pos=(10,320))
		label15.SetFont(font1)
		text15 = wx.TextCtrl(panel,-1,pos=(200,320),size=(50,20))

		label16 = wx.StaticText(panel,-1,"Grade if students answered",pos=(300,165))
		label16.SetFont(font1)
		text16 = wx.TextCtrl(panel,-1,pos=(650,165),size=(50,20))

		label17 = wx.StaticText(panel,-1,"Grade if students did not answered",pos=(300,190))
		label17.SetFont(font1)
		text17 = wx.TextCtrl(panel,-1,pos=(650,190),size=(50,20))

		self.button1 = button1
		self.button2 = button2
		self.button3 = button3
		self.radio3_1 = radio3_1
		self.radio3_2 = radio3_2
		self.radio10_1 = radio10_1
		self.radio10_2 = radio10_2
		self.radio14_1 = radio14_1
		self.radio14_2 = radio14_2
		self.label4 = label4
		self.label5 = label5
		self.label11 = label11
		self.label12 = label12
		self.label13 = label13
		self.text1 = text1
		self.text2 = text2
		self.text4 = text4
		self.text5 = text5
		self.text6 = text6
		self.text7 = text7
		self.text8 = text8
		self.text9 = text9
		self.text11 = text11
		self.text12 = text12
		self.text13 = text13
		self.text15 = text15
		self.text16 = text16
		self.text17 = text17
		self.Bind(wx.EVT_BUTTON,self.OnButton1,self.button1)
		self.Bind(wx.EVT_BUTTON,self.OnButton2,self.button2)
		self.Bind(wx.EVT_RADIOBUTTON,self.OnRadio1,self.radio3_1)
		self.Bind(wx.EVT_RADIOBUTTON,self.OnRadio2,self.radio3_2)
		self.Bind(wx.EVT_RADIOBUTTON,self.OnRadio3,self.radio10_1)
		self.Bind(wx.EVT_RADIOBUTTON,self.OnRadio4,self.radio10_2)
		frame.Show()
		return True

	def OnRadio1(self,event):
		self.label4.Enable(True)
		self.text4.Enable(True)
		self.label5.Enable(True)
		self.text5.Enable(True)
	def OnRadio2(self,event):
		self.label4.Enable(False)
		self.text4.Enable(False)
		self.label5.Enable(False)
		self.text5.Enable(False)	
	def OnRadio3(self,event):
		self.label11.Enable(True)
		self.text11.Enable(True)
		self.label12.Enable(True)
		self.text12.Enable(True)
		self.label13.Enable(False)
		self.text13.Enable(False)
		self.radio14_1.Enable(False)
		self.radio14_2.Enable(False)
	def OnRadio4(self,event):
		self.label11.Enable(False)
		self.text11.Enable(False)
		self.label12.Enable(False)
		self.text12.Enable(False)
		self.label13.Enable(True)
		self.text13.Enable(True)
		self.radio14_1.Enable(True)
		self.radio14_2.Enable(True)

	def OnButton1(self,event):
		website = self.text1.GetValue()
		excel = self.text2.GetValue()
		account = self.text4.GetValue()
		password = self.text5.GetValue()
		number = int(self.text6.GetValue())
		sheet = int(self.text7.GetValue())
		row1 = int(self.text8.GetValue())
		row2 = int(self.text9.GetValue())
		if self.radio10_2.GetValue() == True:
			way = True
			#error
			col1 = int(self.text13.GetValue())
			if self.radio14_2.GetValue() == True:
				col2 = True
			else:
				col2 = False
		else:
			way = False
			#error
			col1 = int(self.text11.GetValue())
			col2 = int(self.text12.GetValue())
		#error
		col_grade = int(self.text15.GetValue())
		#error
		self.work = InputGrade(website,excel)
		#error
		t1 = threading.Thread(target = self.work.students,args=((account, password, sheet, col1, col2, col_grade, way, row1, row2, number),),)
		t1.setDaemon(True)
		t1.start()
		self.button1.Enable(False)
		
	def OnButton2(self,event):
		self.work.Stop()
		self.button1.Enable(True)

	def OnButton3(self,event):
		website = self.text1.GetValue()
		excel = 1
		account = self.text4.GetValue()
		password = self.text5.GetValue()
		number = int(self.text6.GetValue())
		grade1 = int(self.text16.GetValue())
		grade2 = int(self.text17.GetValue())
		self.work = InputGrade(website,excel)
		t2 = threading.Thread(target = self.work.auto_check,args=((account,password,grade1,grade2,number),),)
		t2.setDaemon(True)
		t2.start()
		self.button3.Enable(False)


app = Grade_GUI()
app.MainLoop()