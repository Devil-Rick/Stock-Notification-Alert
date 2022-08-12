import requests as req
import config
from datetime import date
from datetime import timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# TODO 1: STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)

market_url = "https://www.alphavantage.co/query"
market_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,  # To check increase working change "RKLB"
    "apikey": config.STOCK_API
}
market_response = req.get(market_url, params=market_params)
market_response.raise_for_status()
market_response_data = market_response.json()
stk_price_current = float(market_response_data["Time Series (Daily)"][str(yesterday)]["4. close"])
stk_price_previous = float(market_response_data["Time Series (Daily)"][str(day_before_yesterday)]["4. close"])
percent = (stk_price_previous * 5 / 100)

if (stk_price_current >= stk_price_previous + percent) or (stk_price_current <= stk_price_previous - percent):
    print("Get News")
else:
    print(stk_price_previous, stk_price_current)

# TODO 2: STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# TODO 3: STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
 file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the
  height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required
 to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near 
 the height of the coronavirus market crash.
"""
