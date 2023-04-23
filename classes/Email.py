import os
import math
import imghdr
import smtplib 
import email.message
import constants as CON
from dotenv import load_dotenv

class Email:
	def __init__(self, currencyObjects):
		load_dotenv('.env')
		self.objects = currencyObjects

		self.body = ""
		self.today = self.format_todays_date()

		self.highlighted_currency = 1
		self.highlighted_price = 1

		self.s = smtplib.SMTP('smtp.gmail.com: 587')
		self.s.starttls()

	def authenticate(self):
		# Login Credentials for sending the mails
		password = os.environ['GMAILKEY']
		self.s.login(self.msg['From'], password)

	def format_todays_date(self):
		todays_day = ('000'+str(CON.TODAY.day))[-2:]
		todays_month = ('000'+str(CON.TODAY.month))[-2:]
		todays_year = str(CON.TODAY.year)

		today = todays_day + '/' + todays_month + '/' + todays_year
		return today

	def add_attachments(self):
		for file in os.scandir('graphs'):
			with open(file, 'rb') as image:
				file_data = image.read()
				file_type = imghdr.what(image.name)
				file_name = image.name.split('/')[-1]

				self.msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

	def define_subject(self):
		subject = ""

		for currency in self.objects:
			currencyObject = self.objects[currency]

			subject = subject + "{"+currency+"} "
			subject = subject + f"R${math.ceil(currencyObject.todays_price * 100.0) / 100.0} | "

		return subject + str(CON.TODAY.strftime('%d/%m/%y'))
			
	def send(self, receiver):

		self.msg = email.message.EmailMessage()
		self.msg['Subject'] = self.define_subject()
		self.msg['From'] = os.environ['SENDER']
		self.msg['To'] = receiver
		
		self.msg.add_header ('Content-Type', 'text/html') 
		self.msg.set_payload(self.body)

		self.add_attachments()
		self.authenticate()

		self.s.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string().encode('utf-8'))
		print('Email Sent!')