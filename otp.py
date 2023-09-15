from email.mime.text import MIMEText
import math, random
import smtplib
import pymysql
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
# from email.mime.number import MIMENumber
import smtplib
import random
from email.mime.multipart import MIMEMultipart


# print("             Login Page             ")

# mail=input("Enter Your Mail-id : ")
# password=input("Enter Your Password : ")
# type='Login'

def OTP():
	# number="abcdefghijklmnopqrstuvwxyz"
	number='0123456789'
	pin=""
	for k in range(4):
		pin += number[math.floor(random.random() * 10)]
	return pin
# print("Login OTP : ",OTP())

# conn=pymysql.connect(db='qwerty',host='localhost',user='root',password='admin')
# cur =conn.cursor()
# sql="INSERT INTO qwertydata(email,password,type) VALUES(%s,%s,%s)"
# val=(mail,password,type)
# cur.execute(sql,val)
# account=cur.fetchone()
# conn.commit()
# print("Login Successfully")


# print("             Register Page             ")

# email=input("Enter Your Mail-i'd : ")
# password=input("Enter your pasword : ")

# reg='Register'
# conn=pymysql.connect(db='qwerty',host='localhost',user='root',password='admin')
# cur =conn.cursor()
# sql="INSERT INTO qwertydata(email,password,type) VALUES(%s,%s,%s)"
# val=(email,password,reg)
# # print('2')
# cur.execute(sql,val)
# account=cur.fetchone()
# conn.commit()
# print(sql,val)
# print('Register Successfully')