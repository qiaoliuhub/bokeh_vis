import os
import dotenv
import requests
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

class StockDataRetriever:
    '''
    Retrive data from alpha vantage
    '''
    def __init__(self):
        
        dotenv.load_dotenv()
        self.url = 'https://www.alphavantage.co/query'
        self.alpha_vantage_apikey = os.getenv('ALPHA_VANTAGE_APIKEY')
    
    def get_stock_data_in_json_daily(self, symbol, function = 'TIME_SERIES_DAILY', outputsize = 'compact'):

        '''
        Request the recent stock data from alpha vantage
        :symbol: str
        :function: str
        :outputsize: str, compact and full
        :return: json, the retrived data in json format 
        '''

        request_params = {'function':function,
                        'outputsize':outputsize,
                        'symbol':symbol,
                        'apikey':self.alpha_vantage_apikey}
        json_stock_data = requests.get(self.url, params=request_params)
        print(json_stock_data)
        if json_stock_data.status_code == requests.codes.ok:
            return json_stock_data.json()
        else:
            print('Fail to retrieve data for {0!r}'.format(symbol))
            return None

    def get_stock_data_in_dataframe_daily(self, symbol, function = 'TIME_SERIES_DAILY', outputsize = 'compact'):
        
        '''
        Request the recent stock data from alpha vantage
        :symbol: str
        :function: str, TIME_SERIES_DAILY, 
        :outputsize: str, compact and full
        :return: json, the retrived data in json format 
        '''
        json_data = self.get_stock_data_in_json_daily(symbol, function = function, outputsize = outputsize)        
        if not json_data:
            return None
        keys = list(json_data.keys())
        print(keys)
        stock_data = json_data[keys[1]]
        stock_df = pd.json_normalize(stock_data.values())
        stock_df.index = stock_data.keys()
        # cols = next(iter(stock_data)).keys()
        # stock_df = pd.DataFrame(columns = cols)
        # for key in stock_data.keys():
        #     stock_df.loc[key] = pd.Series(stock_data[key])
        return stock_df
    
class BokenPlotter:

    # select the tools we want
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"
    def __init__(self, symbol, stock_df):
        if isinstance(stock_df, pd.DataFrame):
            self.stock_df = stock_df
        else:
            self.stock_df = pd.read_csv(stock_df, index_col = 0)
        self.stock_df.index = self.stock_df.index.map(lambda x: pd.to_datetime(x, format = '%Y-%m-%d'))
        self.symbol = symbol

    def create_plot_components(self, plot_col = '4. close'):

        # # output to static HTML file
        # output_file("sample.html")
        ## use the boken to build a plot and output the javascript and div component 
        stock_plot = figure(plot_width=800, plot_height=350, x_axis_type="datetime", tools = self.TOOLS)
        ## add renderers
        stock_plot.line(self.stock_df.index, self.stock_df[plot_col], color='green', legend_label=self.symbol)

        stock_plot.title.text = self.symbol + ' Close Prices'
        stock_plot.legend.location = "top_left"
        stock_plot.grid.grid_line_alpha = 0
        stock_plot.xaxis.axis_label = 'Date'
        stock_plot.yaxis.axis_label = 'price'
        stock_plot.ygrid.band_fill_color = "cyan"
        stock_plot.ygrid.band_fill_alpha = 0.1

        # show(stock_plot)
        return components(stock_plot)

if __name__ == '__main__':
     
    # sdr = StockDataRetriever()
    # stock_df = sdr.get_stock_data_in_dataframe_daily('AAPL')
    stock_df = 'data_sample.csv'
    stock_ploter = BokenPlotter('AAPL', stock_df)
    stock_ploter.create_plot_components(plot_col = '4. close')