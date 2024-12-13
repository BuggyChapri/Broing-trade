from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

NEWS_API_GLOBAL_DATA = "https://api.coinlore.net/api/global/"
TICKERS = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
MARKET_COINS = "https://api.coinlore.net/api/coin/markets/?id=90"

NEWS_API_KEY = "0c31e0ef9b1044378a917932afc3b5a6"
URL = f"https://newsapi.org/v2/everything?q=bitcoin&apiKey={NEWS_API_KEY}"


@app.route("/")
def index():
    global_data = Get_Global_Crypto_Data()
    tickers = Tickers()
    market_coins = Market_coins()

    return render_template(
        "index.html",
        get_Global_Crypto_Data=global_data,
        ttickers=tickers,
        market_coins=market_coins,
    )


@app.route("/news")
def news():
    news_data = News()
    return render_template("news.html", ne_ws=news_data)


@app.route("/coin/<int:coin_id>")
def coins(coin_id):
    coin_data = Ticker_sc(coin_id)
    print(f"Selected Coin ID: {coin_id}")
    return render_template("coinweight.html", coin_data=coin_data)

def Get_Global_Crypto_Data():
    response = requests.get(NEWS_API_GLOBAL_DATA)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch global crypto data.")
        return {"error": "Failed to fetch global data"}


def Tickers():
    response = requests.get(TICKERS)
    tickers = []

    if response.status_code == 200:
        data = response.json()
        for i in data["data"]:
            tickers.append({
                "id": i["id"],
                "symbol": i["symbol"],
                "name": i["name"],
                "nameid": i["nameid"],
                "rank": i["rank"],
                "price_usd": i["price_usd"],
                "percent_change_24h": i["percent_change_24h"],
                "percent_change_1h": i["percent_change_1h"],
                "percent_change_7d": i["percent_change_7d"],
                "price_btc": i["price_btc"],
                "market_cap_usd": i["market_cap_usd"],
                "volume24": i["volume24"],
                "csupply": i["csupply"],
                "tsupply": i["tsupply"],
                "msupply": i["msupply"],
            })
    else:
        print("Failed to fetch ticker data.")

    return tickers


def Market_coins():
    response = requests.get(MARKET_COINS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch market coins.")
        return {"error": "Failed to fetch market coins"}


def Ticker_sc(coin_id):
    url = f"https://api.coinlore.net/api/ticker/?id={coin_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch specific coin data.")
        return {"error": "Failed to fetch specific coin data"}


def News():
    response = requests.get(URL)
    news = []
    if response.status_code == 200:
        data = response.json()
        for i in data["articles"]:
            news.append({
                "author": i["author"],
                "title": i["title"],
                "description": i["description"],
                "url": i["url"],
                "urlToImage": i["urlToImage"],
                "publishedAt": i["publishedAt"],
            })
    else:
        print("Failed to fetch news data.")
    return news


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
