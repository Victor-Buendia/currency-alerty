from datetime import timedelta

import constants as CON
import requests
import json
import os

class ApiData:
	"""
	attr: from_currency
	attr: to_currency
	attr: response
	attr: todays_price
	attr: serialized_data
	attr: average_price
	"""
	def __init__(self, from_currency, to_currency):
		self.from_currency = from_currency
		self.to_currency = to_currency

		self.get_time_series(self.from_currency, self.to_currency)
		self.date_and_price_serializer(self.response['result'], self.to_currency)

		self.todays_price = self.serialized_data['prices'][-1]
		self.average_price = sum(self.serialized_data['prices'])/len(self.serialized_data['prices'])

	def get_time_series(self, from_currency, to_currency):
		endDate = CON.TODAY
		startDate = endDate + timedelta(days = -30)

		url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={startDate}&end_date={endDate}&base={from_currency}&symbols={to_currency}"

		headers= {
		"apikey": os.environ['ERDA']
		}

		response = requests.request("GET", url, headers = headers)

		self.response = {'result': json.loads(response.text)
						, 'status_code': response.status_code}

		return self.response

	def date_and_price_serializer(self, data, to_currency):
		dates = []
		prices = []

		for date in data['rates'].keys():
			dates.append(date)
			prices.append((data['rates'][date])[to_currency])

		self.serialized_data = {'dates': dates, 'prices': prices}
			
		return self.serialized_data