# Import Flask and render_template for web app and HTML rendering
from flask import Flask, render_template
# Import nasdaqdatalink for data retrieval from Nasdaq
import nasdaqdatalink
# Import pandas for data manipulation
import pandas as pd
# Import pygal for creating interactive charts
import pygal

# Initialize the Flask application
app = Flask(__name__)

# Set the API key for nasdaqdatalink
nasdaqdatalink.ApiConfig.api_key = 'Cec7CiuhRPZrwYMk4cjY'

# Function to obtain Bitcoin price today
def get_bitcoin_price():
  # Retrieve data from nasdaqdatalink
  data = nasdaqdatalink.get_table('QDL/BCHAIN', code='MKPRU')
  # Obtain the latest date
  date = data.iloc[0,1].strftime('%Y-%m-%d')
  # Obtain the latest market price
  price = data.iloc[0,2]
  # Return date and price
  return date, price

# Function to create a chart
def create_chart(data_code, title, file_name):
  # Retrieve data from nasdaqdatalink
  data = nasdaqdatalink.get_table('QDL/BCHAIN', code=data_code)
  # Initialize an empty list to store date and value tuples
  data_list = []
  # Iterate over the data rows
  for index, row in data.iterrows():
      # Convert the timestamp to a date string in the format %Y-%m-%d
      date = row[1].strftime('%Y-%m-%d')
      # Append the date and value to the data list
      data_list.append((date, row[2]))
  # Extract separate lists for dates and values, and reverse them
  dates, values = zip(*data_list)
  dates = list(dates)[::-1]
  values = list(values)[::-1]
  # Create a line chart using pygal
  chart = pygal.Line(x_labels_major_every=150, show_minor_x_labels=False)
  chart.title = title
  chart.x_labels = dates
  chart.add('Values', values)
  # Render the chart to a file
  chart.render_to_file(file_name)

# Create the charts for the specified data codes and save them as SVG files in the templates folder
create_chart('TVTVR', 'Bitcoin Trade Volume vs Transaction Volume Ratio', 'templates/bitcoin_trade_volume_vs_transaction_volume_ratio.svg')
create_chart('NTRAN', 'Bitcoin Number of Transactions', 'templates/bitcoin_number_transactions.svg')

# Define the route for the homepage
@app.route('/')
def index():
  # Obtain the latest price and date
  date, price = get_bitcoin_price()
  # Format the price in accounting format
  price = "${:,.2f}".format(price)
  # Render the index.html template
  return render_template('index.html', date=date, price=price)

# Run the Flask application
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)