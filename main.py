import os
import json
import constants as CON
from dotenv import load_dotenv

from classes.ApiData import ApiData
from classes.Email import Email
from classes.Graph import Graph

global objects
objects = {}

def execute(from_currency, to_currency):
	currencyObj = ApiData(from_currency, to_currency)

	if currencyObj.response['status_code'] == 200:
		if currencyObj.todays_price < currencyObj.average_price or CON.FORCEALL:
			objects[currencyObj.from_currency] = currencyObj
			Graph(currencyObj)
	else:
		raise Exception(f'INFO:::::: API connection error for {currencyObj.from_currency}.')

if __name__ == '__main__':
	load_dotenv('.env')
	os.mkdir('graphs')

	to_currency = 'BRL'
	from_currency = list(CON.names.keys())

	for currency in from_currency:
		execute(currency, to_currency)

	receivers = json.loads(os.environ['RECEIVERS'])
	email = Email(objects)
	for receiver in receivers:
		email.send(receiver)
