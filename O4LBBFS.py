from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
from talib import BBANDS
from talib import SMA
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter
print("ONLY FOR LEGENDS SIGNALS 0.02_300_1")
account = input("Email :")
password = input("password :")
goal = input("Goal  :")
I_want_money = IQ_Option(account, password)
check = I_want_money.connect()
now = datetime.now()
if check:
        print("####   CONNECT  SUCCEFULY    #####")
else:
        print("connect failed")
def send_msj(message):
    webhook = Webhook.from_url("https://discord.com/api/webhooks/989158059022618655/hgkfCPkxufy_j5xmUsBG76ZslDftZc1sAZlpwjSXckvcMdlLnLwylHGPcn0r1K6lQQ1X", adapter=RequestsWebhookAdapter())
    webhook.send(message)
print(f"##connect to {goal}")
size = 300
maxdict = 200
I_want_money.start_candles_stream(goal, size, maxdict)
current_time = now.strftime("%H:%M:%S:")
while True:
    if now.strftime("%H") >= "08" and now.strftime("%H") <= "17":
        time.sleep(0.25)
        candles = I_want_money.get_realtime_candles(goal, size)
        inputs = {
            'open': np.array([]),
            'close': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
        }
        for timestamp in list(candles.keys()):
            open = inputs["open"] = np.append(inputs["open"], candles[timestamp]["open"])
            close = inputs["close"] = np.append(inputs["open"], candles[timestamp]["close"])
            high = inputs["high"] = np.append(inputs["open"], candles[timestamp]["max"])
            low = inputs["low"] = np.append(inputs["open"], candles[timestamp]["min"])
        upperband, middleband, lowerband = BBANDS(close * 1000000, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        real_200 = SMA(close, timeperiod=200)
        up = upperband[-1]
        dn = lowerband[-1]
        md = middleband[-1]
        cls = close[-1] * 1000000
        rl_200 = real_200[-1] * 1000000
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:")
        if up < rl_200:
            if cls > up or cls == up :
                send_msj(f"## Sell STR BB {goal} ##{current_time} ")
                print(f"# Sell {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn} ")
                time.sleep(size)
                continue
        if dn > rl_200:
            if cls < dn or cls == dn:
                send_msj(f"## Buy STR BB {goal} ##{current_time}")
                print(f"# Buy {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn}")
                time.sleep(size)
                continue
        if now.strftime("%S") == "00" :
            print(f"# {goal}||| Close : {cls} ||| {current_time}||| UP : {up} || MV_200 : {rl_200} || DN : {dn}")
       
    else :
        print(f"################# SESSION IS OVER FOR THIS DAY ################# ")  
        time.sleep(60)     
