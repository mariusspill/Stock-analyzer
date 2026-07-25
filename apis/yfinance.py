import yfinance as yf

ticker = "IBM"

lst = ["IBM", "JNJ", "DG"]

y_ticker = yf.Ticker(ticker)

df = y_ticker.history(start="2020-01-01", end= "2026-01-01")
data = yf.download(lst, start="2025-01-01", end="2025-02-01")

print(df[(df["Dividends"] > 0 or df["Stock Splits"] > 0)])
print(data["Open"]["JNJ"])