from flask import Flask, render_template, request, redirect
from stocks_data import StockDataRetriever, BokenPlotter
from bokeh.resources import CDN
import dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/graph', methods = ['POST'])
def graph():
  ticker = request.form.get('ticker')
  print(ticker)
  sdr = StockDataRetriever()
  stock_df = sdr.get_stock_data_in_dataframe_daily(ticker)
  boken_plotter = BokenPlotter(symbol=ticker, stock_df=stock_df)
  stock_plot_js, stock_plot_div = boken_plotter.create_plot_components()
  print(stock_plot_div)
  return render_template('graph.html', resources = CDN.render(), stock_plot_script = stock_plot_js, plot_div = stock_plot_div)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  dotenv.load_dotenv()
  port_number = os.getenv('PORT')
  app.run(port=port_number)
