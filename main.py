import requests as req
import config
from newsapi import NewsApiClient
from datetime import date
from datetime import timedelta
from twilio.rest import Client

STOCK_LIST = ["TSLA", "INFY"]  # input all the req stock names
COMPANY_LIST = ["Tesla", "Infosys Limited"]  # input all corresponding company names
MSG_TEXT_LIST = []


# ---------------------- Required Functions ------------------------ #
def send_msg(msg: str):
    # ---------------------- Sending the message ------------------------ #
    msg_text = "\n".join(MSG_TEXT_LIST)
    client = Client(config.TWILIO_ID, config.TWILIO_API)
    message = client.messages.create(
        body=f"{msg_text}{msg}",
        from_='+13149123008',
        to='+918016323773'
    )
    print(message.status)


# ---------------------- Getting the date ------------------------ #
today = date.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = yesterday - timedelta(days=1)

# ---------------------- Setting the Stock API ------------------------ #
# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ONGC&apikey=2EIMT3KDPHRHLY6L
for i in range(len(STOCK_LIST)):
    STOCK = STOCK_LIST[i]
    COMPANY_NAME = COMPANY_LIST[i]
    print(STOCK, len(STOCK_LIST))
    market_url = "https://www.alphavantage.co/query"
    market_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": config.STOCK_API
    }

    market_response = req.get(market_url, params=market_params)
    market_response.raise_for_status()
    market_response_data = market_response.json()
    stk_price_current = float(market_response_data["Time Series (Daily)"][str(yesterday)]["4. close"])
    stk_price_previous = float(market_response_data["Time Series (Daily)"][str(day_before_yesterday)]["4. close"])
    percent_change = round(((stk_price_current - stk_price_previous) / stk_price_current) * 100, 3)
    if percent_change > 0:
        MSG_TEXT_LIST.append(f"{STOCK} : 🔺 {percent_change}")
    elif percent_change < 0:
        MSG_TEXT_LIST.append(f"{STOCK} : 🔻 {percent_change}")

    # ---------------------- Setting the News API ------------------------ #
    newsapi = NewsApiClient(api_key=config.NEWS_API)
    all_articles = newsapi.get_everything(q=COMPANY_NAME,
                                          domains="cnbc.com, financialexpress.com",
                                          from_param=str(day_before_yesterday),
                                          to=str(today),
                                          language='en',
                                          sort_by='relevancy')

    # ---------------------- Checks the Percent and sends req msg ------------------------ #
    if percent_change > 5:
        total_articles = len(all_articles["articles"])
        if total_articles >= 3:
            for news in range(3):
                MSG_TEXT_LIST.append(f'Headline: {all_articles["articles"][news]["title"]}')
                MSG_TEXT_LIST.append(f'Brief: {all_articles["articles"][news]["content"].partition("+")[0][:-1]}\n')
                send_msg("")
        elif 0 < total_articles < 3:
            for news in range(len(all_articles["articles"])):
                MSG_TEXT_LIST.append(f'Headline: {all_articles["articles"][news]["title"]}')
                MSG_TEXT_LIST.append(f'Brief: {all_articles["articles"][news]["content"].partition("+")[0][:-1]}\n')
                send_msg("")
        else:
            send_msg(f"\nNo Breaking News Available for {COMPANY_NAME}")
    else:
        print("working")
