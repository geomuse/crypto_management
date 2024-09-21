from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import json , requests
from IPython.display import display

app = Flask(__name__)

# Extract and structure data
def extract_data(data):
    cryptos = []
    for item in data:
        cryptos.append({
            'Name': item['name'],
            'Symbol': str(item['symbol']).upper(),
            'Current Price': str(np.round(float(item['current_price']),3)),
            'Market Cap': str(float(item['market_cap'])),
            '24h Change (%)': item['price_change_percentage_24h'],
            'Circulating Supply': str(np.round(float(item['circulating_supply']),3))
            # 'Last Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return cryptos

def background_color(val):
    color = 'background-color: #e74c3c' if val > 0 else 'background-color: #2ecc71'
    return color

@app.route('/', methods=['GET', 'POST'])
def index():

    url = "https://api.coingecko.com/api/v3/coins/markets"
    parameters = {
        'vs_currency': 'usd',
        # 'ids': 'bitcoin,ethereum,tether,dogecoin,xrp,tron',
        'order': 'market_cap_desc',
        'per_page': 50,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage' : '24h'
    }

    # Make the request
    response = requests.get(url, params=parameters)

    data = response.json()
    crypto_data = extract_data(data)
    df = pd.DataFrame(crypto_data)
    
    styled_df = df.style.map(background_color, subset=['24h Change (%)'])

    coin_chart = styled_df.to_html(classes='table table-striped',index=False)
    
    # display(styled_df)
    custom_chart = \
    """
    <style>
        table {
            border-collapse : collapse;
            width : 100% ;
            letter-spacing: 0.5px;
            text-align : center ; 
        }
    </style>
    """
    final_html = custom_chart + coin_chart

    return render_template('result.html',coin_chart=final_html)

if __name__ == '__main__':
    
    app.run(debug=True)