import math
import constants as CON
import matplotlib.pyplot as plt

class Graph:
	def __init__(self, currencyObject):
		self.ax = self.create_graph(10, 6)
		self.draw_graph(currencyObject)

	def create_graph(self, x_size, y_size):
		fig, ax = plt.subplots(figsize = (x_size, y_size))
		return ax

	def draw_avg_and_today_lines(self, currencyObject, dates_v):
		today_line_v = []
		avg_line_v = []

		for date in dates_v:
			today_line_v.append(currencyObject.todays_price)
			avg_line_v.append(currencyObject.average_price)

		return today_line_v, avg_line_v

	def plots(self, dates_v, prices_v, today_line_v, avg_line_v):
		# Graph Prices
		self.ax.plot(dates_v, prices_v, 'r')
		# Graph Dots Prices
		self.ax.plot(dates_v, prices_v, 'r.')
		# Today's Price
		self.ax.plot(dates_v, today_line_v, '--g')
		# Average Price
		self.ax.plot(dates_v, avg_line_v, ':k')

	def draw_graph(self, currencyObject):
		dates_v, prices_v = currencyObject.serialized_data['dates'], currencyObject.serialized_data['prices']

		today_line_v, avg_line_v = self.draw_avg_and_today_lines(currencyObject, dates_v)

		today_formatted = CON.TODAY.strftime('%d/%m/%y')
		title = f"Cotação {CON.names[currencyObject.from_currency]} | " + today_formatted

		plt.title(title, size = 15)
		self.ax.set(frame_on = False)

		self.plots(dates_v, prices_v, today_line_v, avg_line_v)

		labels = self.ax.get_xticklabels()
		plt.setp(labels
				, rotation = 45 
				, horizontalalignment = 'right')
		self.ax.yaxis.set_major_formatter('R${x:1.2f}')

		# Label for today's price
		self.ax.text(dates_v[-1]
				, prices_v[-1]
				, '   HOJE: R$'+str(math.ceil(prices_v[-1]*100)/100), size = 10)
		# Label for average price
		self.ax.text(dates_v[-1]
				, avg_line_v[-1]
				, '   MÉDIA: R$'+str(math.ceil(avg_line_v[-1]*100)/100), size = 10)

		plt.tight_layout()
		plt.savefig(f"graphs/{currencyObject.from_currency}_graph.png", bbox_inches = "tight")

	def show_plot(self):
		self.ax.show()