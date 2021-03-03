import requests
from twilio.rest import Client

STOCK_NAME = "stock name you want to check goes here"
COMPANY_NAME = "company name you want to check goes here"
STOCK_API_KEY = 'https://www.alphavantage.co api key goes here'
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "https://newsapi.org api key goes here"

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
}
# get request to alphavantage api
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)

stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
# getting yesterdays tesla closing price
yesterday_closing_price = data_list[0]["4. close"]
# getting the day before yesterday tesla closing price
day_before_yesterday_closing_price = data_list[1]["4. close"]
# calculating the difference in the stock price
stock_price_difference = abs(float(day_before_yesterday_closing_price) - float(yesterday_closing_price))
# calculation the difference in the stock price but in %
stock_price_percentage_difference = (stock_price_difference / float(day_before_yesterday_closing_price)) * 100

#check if stock price percentage difference is more than +3% or -3%
if stock_price_percentage_difference > 3:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    # get request to newsapi api
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    # getting first three articles about company
    newest_articles = news_response.json()["articles"][:3]
    print(newest_articles)

    formatted_newest_article = [f'Headline:{article["title"]} \n Brief:{article["description"]}' for article in
                                newest_articles]
    account_sid = 'YOUR TWILIO ACCOUNT_SID'
    auth_token = 'YOUR TWILIO AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    # sending a message to myself with alert that there was a  price change in their stock
    # with three newest articles from newsapi
    for article in formatted_newest_article:
        message = client.messages \
            .create(
            body=f"{article}",
            from_='HERE GOES YOUR TWILIO PHONE NUMBER',
            to='HERE GOES THE NUMBER YOU WANT TO NOTIFY'
        )
