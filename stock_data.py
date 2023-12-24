import yfinance as yf

def get_stockData(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

