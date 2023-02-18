import imghdr
import smtplib 
import email.message
from datetime import date, timedelta
import os
import requests
import json
import math
import matplotlib.pyplot as plt

def enviar_email(body, precoHoje, receiver):
	corpo_email =\
	f"""
	"""

	msg = email.message.EmailMessage()
	msg['Subject'] = "{EUR} "+f"R${math.ceil(precoHoje * 100.0) / 100.0} | " +('000'+str(date.today().day))[-2:]+'/'+('000'+str(date.today().month))[-2:]+'/'+str(date.today().year)
	msg['From'] = os.environ['SENDER']
	msg['To'] = receiver
	password = os.environ['GMAILKEY']
	msg.add_header ('Content-Type', 'text/html') 
	msg.set_payload(corpo_email)

	with open("eurograph.png", 'rb') as imagem:
		file_data = imagem.read()
		file_type = imghdr.what(imagem.name)
		file_name = imagem.name

	msg.add_attachment(file_data, maintype = "image", subtype = file_type, filename = file_name)

	s = smtplib.SMTP('smtp.gmail.com: 587')
	s.starttls()

	# Login Credentials for sending the mails
	s.login(msg['From'], password)
	s.sendmail(msg['From'], msg['To'], msg.as_string().encode ('utf-8'))
	print('Emails enviados')

def preco_euro(fromc, toc):
	url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={date.today()+timedelta(days = -30)}&end_date={date.today()}&base={fromc}&symbols={toc}"

	payload = {}
	headers= {
	"apikey": os.environ['ERDA']
	}

	response = requests.request("GET", url, headers=headers, data = payload)

	status_code = response.status_code
	result = response.text

	return result, status_code

def cria_grafico(data):
	info = data

	dates = []
	values = []
	today = []
	avg = []

	for i in info['rates'].keys():
		dates.append(i)
		values.append(info['rates'][i]['BRL'])
		
	for i in dates:
		today.append(values[-1])
		avg.append(sum(values)/len(values))
		
	fig, ax = plt.subplots(figsize=(10, 6))

	plt.title("Cotação do Euro | "+date.today().strftime('%d/%m/%y'), size=15)
	ax.set(frame_on=False)

	ax.plot(dates, values, 'r')
	ax.plot(dates, values, 'r.')
	ax.plot(dates, today, '--g')
	ax.plot(dates, avg, ':k')

	labels = ax.get_xticklabels()
	plt.setp(labels, 
			rotation=45, 
			horizontalalignment='right')
	ax.yaxis.set_major_formatter('R${x:1.2f}')

	ax.text(dates[-1], values[-1], '   HOJE: R$'+str(math.ceil(values[-1]*100)/100), size=10)
	ax.text(dates[-1], avg[-1], '   MÉDIA: R$'+str(math.ceil(avg[-1]*100)/100), size=10)

	plt.tight_layout()
	plt.savefig("eurograph.png", bbox_inches="tight")
	return avg[-1]
	# plt.show()

if __name__ == '__main__':
	precos = json.loads(preco_euro('EUR', 'BRL')[0])
	
	precoHoje = precos['rates'][str(date.today())]['BRL']

	avg = cria_grafico(precos)

	if precoHoje < avg:
		receivers = json.loads(os.environ['RECEIVERS'])
		for receiver in receivers:
			enviar_email(precos, precoHoje, receiver)