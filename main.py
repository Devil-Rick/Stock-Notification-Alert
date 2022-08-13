import requests as req
import config
from newsapi import NewsApiClient
from datetime import date
from datetime import timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

# ---------------------- Getting the date ------------------------#
today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)

# ---------------------- Setting the Stock API ------------------------#
market_url = "https://www.alphavantage.co/query"
market_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "RKLB",  # To check increase working change "RKLB"
    "apikey": config.STOCK_API
}
market_response = req.get(market_url, params=market_params)
market_response.raise_for_status()
market_response_data = market_response.json()
stk_price_current = float(market_response_data["Time Series (Daily)"][str(yesterday)]["4. close"])
stk_price_previous = float(market_response_data["Time Series (Daily)"][str(day_before_yesterday)]["4. close"])
percent_change = round(((stk_price_current - stk_price_previous) / stk_price_current) * 100, 3)
if percent_change > 0:
    print(f"{STOCK} : 🔺{abs(percent_change)}")
elif percent_change < 0:
    print(f"{STOCK} : 🔻{abs(percent_change)}")

# ---------------------- Setting the News API ------------------------#
newsapi = NewsApiClient(api_key=config.NEWS_API)
all_articles = newsapi.get_everything(q=COMPANY_NAME, domains="cnbc.com, financialexpress.com",
                                      from_param='2022-08-01',
                                      to='2022-08-12',
                                      language='en',
                                      sort_by='relevancy')

percent = (stk_price_previous * 5 / 100)
if (stk_price_current >= stk_price_previous + percent) or (stk_price_current <= stk_price_previous - percent):
    for i in range(3):
        print(f'Headline: {all_articles["articles"][i]["title"]}')
        print(f'Brief: {all_articles["articles"][i]["content"].partition("[")[0]}\n')

# ---------------------- Sending the message ------------------------#
# TODO 1: STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
