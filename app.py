from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy
import requests  

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

NEWS_API_GLOBAL_DATA = "https://api.coinlore.net/api/global/"
TICKERS = "https://api.coinlore.net/api/tickers/?start=200&limit=100"
MARKET_COINS = " https://api.coinlore.net/api/coin/markets/?id=90"

@app.route("/")
def index():
    get_Global_Crypto_Data = Get_Global_Crypto_Data() 
    ttickers = Tickers()
    market_coins = Market_coins()
    return render_template("index.html", get_Global_Crypto_Data = get_Global_Crypto_Data, ttickers = ttickers, market_coins = market_coins)

def Get_Global_Crypto_Data():
    response = requests.get(NEWS_API_GLOBAL_DATA)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"SORRY"}
    
def Tickers():
    response = requests.get(TICKERS)
    tickers = []  
    
    if response.status_code == 200:
        data = response.json()
        for i in data["data"]:
            symbol = i["symbol"]
            name = i["name"]
            nameid = i["nameid"]
            rank = i["rank"]
            price_usd = i["price_usd"]
            percent_change_24h = i["percent_change_24h"]
            percent_change_1h = i["percent_change_1h"]
            percent_change_7d = i["percent_change_7d"]
            price_btc = i["price_btc"]
            market_cap_usd = i["market_cap_usd"]
            volume24 = i["volume24"]
            csupply = i["csupply"]
            tsupply = i["tsupply"]
            msupply = i["msupply"]
            
            tickers.append({
                "symbol": symbol,
                "name": name,
                "nameid": nameid,
                "rank": rank,
                "price_usd": price_usd,
                "percent_change_24h": percent_change_24h,
                "percent_change_1h": percent_change_1h,
                "percent_change_7d": percent_change_7d,
                "price_btc": price_btc,
                "market_cap_usd": market_cap_usd,
                "volume24": volume24,
                "csupply": csupply,
                "tsupply": tsupply,
                "msupply": msupply
            })        
    else:
        print("SORRY")

    return tickers

def Market_coins():
    response = requests.get(MARKET_COINS)
    market_coins = []
    if response.status_code == 200:
        return response.json()
    else:
        print("BAD GATEWAY OR SORRY")



if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug = True)