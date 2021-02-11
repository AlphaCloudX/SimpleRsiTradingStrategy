from yahoo_fin.stock_info import *
from twelvedata import TDClient
import time
from datetime import datetime

with open("apiKey.txt") as f:
    apiKey = f.readline()

# Test out for best results
overSoldLine = 47
overBoughtLine = 59

# Dynamic Variables
boughtState = False
stockOwned = 0
bal = 10000
percentageRiskPerTrade = 0.2

while True:

    try:
        # Initiliaze client -api key
        td = TDClient(apikey=apiKey)
        ts = td.time_series(
            symbol="CAD/USD",
            interval="5min",
            outputsize=1,
            timezone="America/New_York"
        )
        # Returning Json
        df = ts.with_rsi().as_json()
        print("------")
        print(get_live_price("CADUSD=X"))
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)
        print("Rsi: ")
        print(df[0]["rsi"])

        rsiNumber = float(df[0]["rsi"])

        # Buying Method
        if boughtState is not True:
            if float(rsiNumber) <= overSoldLine:
                boughtState = True

                amountSharesBought = float((bal * 0.02) / float(get_live_price("CADUSD=X")))
                bal = float(bal - (amountSharesBought * float(get_live_price("CADUSD=X"))))

        # Selling Method
        if boughtState is True:
            if float(rsiNumber) >= overBoughtLine:
                bal = float(bal + (amountSharesBought * float(get_live_price("CADUSD=X"))))
                amountSharesBought = 0
                boughtState = False

        print("Bal: ")
        print(bal)
        time.sleep(300)

    except:
        print("Request Limit Reached")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)
        break