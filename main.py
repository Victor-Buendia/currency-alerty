import os
import math
import json
import imghdr
import smtplib 
import requests
import email.message
import matplotlib.pyplot as plt
from datetime import date, timedelta

global today
today = date.today()

def load_json(json_data):
	return json.loads(json_data)

def send_email(todays_price, receiver):
	corpo_email =\
	f"""
	"""
	
	rounded_todays_price = math.ceil(todays_price * 100.0) / 100.0
	todays_day = ('000'+str(date.today().day))[-2:]
	todays_month = ('000'+str(date.today().month))[-2:]
	todays_year = str(date.today().year)
	today = todays_day + '/' + todays_month + '/' + todays_year

	msg = email.message.EmailMessage()
	msg['Subject'] = "{EUR} " + f"R${rounded_todays_price} | " + today
	msg['From'] = os.environ['SENDER']
	msg['To'] = receiver
	
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
	password = os.environ['GMAILKEY']
	s.login(msg['From'], password)

	s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))

	print('Email Sent!')

def get_time_series(from_currency, to_currency):
	endDate = date.today()
	startDate = endDate +timedelta(days = -30)

	url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={startDate}&end_date={endDate}&base={from_currency}&symbols={to_currency}"

	payload = {}
	headers= {
	"apikey": os.environ['ERDA']
	}

	response = requests.request("GET", url, headers = headers, data = payload)

	status_code = response.status_code
	result = response.text

	return {'result': result, 'status_code': status_code}

def average(list):
	return sum(list)/len(list)

def data_to_dict(data_dict, to_currency):
	dates = []
	prices = []

	data = load_json(data_dict['result'])

	for date in data['rates'].keys():
		dates.append(date)
		prices.append((data['rates'][date])[to_currency])
		
	return {'dates': dates, 'prices': prices}

def create_graph(x_size, y_size):
	fig, ax = plt.subplots(figsize = (x_size, y_size))
	return fig, ax

def draw_graph(dict_data):
	dates, prices = dict_data['dates'], dict_data['prices']

	average_price = average(prices)
	todays_price = prices[-1]

	today_list = []
	avg_list = []

	for date in dates:
		today_list.append(todays_price)
		avg_list.append(average_price)

	_, ax = create_graph(10, 6)

	today_date = today.strftime('%d/%m/%y')
	title = "Cotação do Euro | " + today_date

	plt.title(title, size = 15)
	ax.set(frame_on = False)

	# Graph Prices
	ax.plot(dates, prices, 'r')
	# Graph Dots Prices
	ax.plot(dates, prices, 'r.')
	# Today's Price
	ax.plot(dates, today_list, '--g')
	# Average Price
	ax.plot(dates, avg_list, ':k')

	labels = ax.get_xticklabels()

	plt.setp(labels
	  		, rotation = 45 
			, horizontalalignment = 'right')
	ax.yaxis.set_major_formatter('R${x:1.2f}')

	# Label for today's price
	ax.text(dates[-1]
	 		, prices[-1]
			, '   HOJE: R$'+str(math.ceil(prices[-1]*100)/100), size = 10)
	# Label for average price
	ax.text(dates[-1]
			, avg_list[-1]
			, '   MÉDIA: R$'+str(math.ceil(avg_list[-1]*100)/100), size = 10)

	plt.tight_layout()
	plt.savefig("eurograph.png", bbox_inches = "tight")

	# plt.show()

def get_today_price(loaded_data, today, to_currency):
	return loaded_data['rates'][str(today)][to_currency]

if __name__ == '__main__':
	from_currency = 'EUR'
	to_currency = 'BRL'

	data = get_time_series(from_currency, to_currency)
	today = date.today()

	if data['status_code'] == 200:
		loaded_data = load_json(data['result'])
		dict_data = data_to_dict(data, to_currency)

		todays_price = get_today_price(loaded_data, today, to_currency)
		average_price = average(dict_data['prices'])

		draw_graph(dict_data)

		if todays_price < average_price:
			receivers = json.loads(os.environ['RECEIVERS'])
			for receiver in receivers:
				send_email(todays_price, receiver)
	else:
		raise Exception('API connection error.')