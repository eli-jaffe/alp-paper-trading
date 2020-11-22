import os
import requests
import json
import time

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': os.environ.get('APCA_API_KEY_ID'), 'APCA-API-SECRET-KEY': os.environ.get('APCA_API_SECRET_KEY')}

 

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)

def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)

#response = create_order("MDB", 100, "buy", "market", "day")

def get_positions():
    r = requests.get("{}/v2/positions".format(BASE_URL), headers=HEADERS)

    return json.loads(r.content)
orders = get_orders()

print(orders)

#response = get_account()
#response = get_positions()
# print(orders[0]['id'])

# set up email connection
# import the smtplib module. It should be included in Python by default
# import smtplib
# set up the SMTP server
# s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
# s.starttls()
# s.login(MY_ADDRESS, PASSWORD)
###

# input target percent increase at which to trade (0.XX format)
TARGET_PERCENT = 0.01
def try_trades():
    while True:
        positions = get_positions()
        if positions:
            for i in positions:
                curr = i['current_price']
                buy_price = i['avg_entry_price']
                print(curr, buy_price)
                if (curr/(1 + TARGET_PERCENT) >= buy_price):
                    response = create_order(i['symbol'],i['qyt'],"sell",'market','gtc')
                    print(response)

                    #send email notification (alpaca might do this automatically)
        else:
            print("You do not currently hold any positions")

        time.sleep(15)

# try_trades()
