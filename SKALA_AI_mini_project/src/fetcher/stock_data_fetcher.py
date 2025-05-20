import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker: str, company_name: str, period="1y", interval="1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError(f"{company_name}에 대한 데이터를 가져올 수 없습니다. 티커: {ticker}, 기간: {period}, 간격: {interval}")
    
    os.makedirs("raw", exist_ok=True)
    path = f"raw/{company_name}.csv"
    df.to_csv(path)
    print(f"[✓] {company_name} 주가 데이터를 '{path}'에 저장했습니다.")
    return df