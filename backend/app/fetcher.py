import json
from moexalgo import Ticker
from datetime import datetime, timedelta

def load_metadata():
    with open('metadata/tickers.json') as f:
        return json.load(f)

def fetch_all_tickers():
    metadata = load_metadata()
    result = []
    end_date = datetime.now().date() - timedelta(days=1)
    
    for ticker_symbol, info in metadata.items():
        try:
            ticker = Ticker(ticker_symbol)
            candles = list(ticker.candles(date=end_date, interval='1d'))
            if not candles:
                continue
            last = candles[-1]
            close_price = last['close']
            open_price = last['open']
            change = ((close_price - open_price) / open_price) * 100
            shares = info['shares_outstanding']
            market_cap = close_price * shares
            
            result.append({
                "ticker": ticker_symbol,
                "sector": info['sector'],
                "price": round(close_price, 2),
                "change": round(change, 2),
                "market_cap": round(market_cap / 1e9, 2),  # млрд
            })
        except Exception as e:
            print(f"Ошибка {ticker_symbol}: {e}")
    
    return result