import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime as dt
import plotly.graph_objects as go



start = dt(1999,1,22)
end = dt.today().date()

# fetch data
nvda = yf.download('NVDA', start, end)

# Calculating moving average (50 day moving average)
nvda['50_MA'] = nvda['Close'].rolling(window=50).mean()

# calculating Bollinger Bonds
# Middle Band (20-day ma)
nvda['20_SMA'] = nvda['Close'].rolling(window=20).mean()
# standard deviation over the same period
nvda['20_STDV'] = nvda['Close'].rolling(window=20).std()

# calculating upper and lower bollinger bands
nvda['Upper_Band'] = nvda['20_SMA'] + (nvda['20_STDV'] * 2)
nvda['Lower_Band'] = nvda['20_SMA'] - (nvda['20_STDV'] * 2)


# Plotting the chart
style.use('ggplot')
plt.figure(figsize=(12,6))
plt.plot(nvda['50_MA'], label = '50-Day Moving Average', color = 'black')
plt.plot(nvda['20_SMA'], label='20-Day SMA', color='orange')
plt.plot(nvda['Upper_Band'], label='Upper Bollinger Band', color='green')
plt.plot(nvda['Lower_Band'], label='Lower Bollinger Band', color='green')
plt.fill_between(nvda.index, nvda['Upper_Band'], nvda['Lower_Band'], color='gray', alpha=0.3)
plt.title("NVIDIA")
plt.ylabel('Price USD', fontsize = 12)
# X Label is automatically generated
plt.legend()

plt.show()

# nvda = yf.Ticker("NVDA")

##  balance sheet and dividends
# print(nvda.quarterly_balancesheet)
# print()
# print(nvda.dividends)

# # transfer balance sheet to excel
# balance_sheet_df = nvda.quarterly_balancesheet
# balance_sheet_df.to_excel("NVDA_data.xlsx")

# # transfer dividends to excel
# dividends_df = nvda.dividends
# dividends_df.to_excel("NVDA_data.xlsx")