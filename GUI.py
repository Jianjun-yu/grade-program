#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-26 21:16:43
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import wx
# import InputGrade


class Grade_GUI(wx.App):
	def OnInit(self):
		print (wx.__file__)
		frame = wx.Frame(parent=None,title="Input Students' Grade",size=(800,500))
		panel = wx.Panel(frame,-1)
		font1 = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
		button1 = wx.Button(panel,-1,"Input Grade",(300,380))

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

		self.button1 = button1
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
		self.Bind(wx.EVT_BUTTON,self.OnButton1,self.button1)
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
			col1 = int(self.text13.GetValue())
			if self.radio14_2.GetValue() == True:
				col2 = True
			else:
				col2 = False
		else:
			way = False
			col1 = int(self.text11.GetValue())
			col2 = int(self.text12.GetValue())
		col_grade = int(self.text15.GetValue())
		print (website)
		print (type(website))
		print (excel)
		print (type(excel))
		print (account)
		print (type(account))
		print (len(account))
		print (password)
		print (type(password))
		print (number)
		print (type(number))
		print (sheet)
		print (type(sheet))
		print (row1)
		print (type(row1))
		print (row2)
		print (type(row2))
		print (col1)
		print (type(col1))
		print (col2)
		print (type(col2))
		print (col_grade)
		print (type(col_grade))
		print(way)
		print(type(way))
		print (self.radio10_2.GetValue())

app = Grade_GUI()
app.MainLoop()