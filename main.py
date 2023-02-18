import smtplib 
import email.message
from datetime import date
import os
import requests
import json
import math

def enviar_email(body, receiver):
	corpo_email =\
	f"""
	{body}
	"""

	msg = email.message.Message()
	msg['Subject'] = "{EUR} "+f"R${math.ceil(body['result'] * 100.0) / 100.0} | " +('000'+str(date.today().day))[-2:]+'/'+('000'+str(date.today().month))[-2:]+'/'+str(date.today().year)
	msg['From'] = os.environ['SENDER']
	msg['To'] = receiver
	password = os.environ['GMAILKEY']
	msg.add_header ('Content-Type', 'text/html') 
	msg.set_payload(corpo_email)

	s = smtplib.SMTP('smtp.gmail.com: 587')
	s.starttls()

	# Login Credentials for sending the mails
	s.login(msg['From'], password)
	s.sendmail(msg['From'], msg['To'], msg.as_string().encode ('utf-8'))
	print('Emails enviados')

def preco_euro(fromc, toc, amount):
	url = f"https://api.apilayer.com/exchangerates_data/convert?to={toc}&from={fromc}&amount={amount}"

	payload = {}
	headers= {
	"apikey": os.environ['ERDA']
	}

	response = requests.request("GET", url, headers=headers, data = payload)

	status_code = response.status_code
	result = response.text

	return result, status_code

if __name__ == '__main__':
	preco = json.loads(preco_euro('EUR', 'BRL', '1')[0])

	receivers = json.loads(os.environ['RECEIVERS'])
	for receiver in receivers:
		enviar_email(preco, receiver)