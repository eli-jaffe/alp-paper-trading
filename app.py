import os
import requests
import json
import time

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': os.environ.get('APCA_API_KEY_ID'), 'APCA-API-SECRET-KEY': os.environ.get('APCA_API_SECRET_KEY')}

# A list of stock tickers that are meant for long term gains and should be exluded from percent gain based script
LONG_TERM = ['ABNB']

# change this depending on your targetpercent
TARGET_PERCENT = 0.05

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

def get_positions():
    r = requests.get("{}/v2/positions".format(BASE_URL), headers=HEADERS)

    return json.loads(r.content)

#print(orders)
#time.sleep(15)
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


def try_trades():
    positions = get_positions()
    if positions:
        for i in positions:
            # exclude long term plays
            if i['symbol'] in LONG_TERM:
                continue
            curr = float(i['current_price'])
            buy_price = float(i['avg_entry_price'])
            print("Stock: " + i['symbol'] + ", Current price: " + str(curr) + ", Buy price: " + str(buy_price) + ", Percent change: " + str(curr/buy_price*100))
            if (curr/(1 + TARGET_PERCENT) >= buy_price):
                response = create_order(i['symbol'],i['qty'],"sell",'market','day')
                print("Order created to sell " + response['qty'] + " stocks of " + response['symbol'])

                #send email notification (alpaca might do this automatically)"""
    else:
        print("You do not currently hold any positions")

while True:
    try_trades()
    time.sleep(1200)
