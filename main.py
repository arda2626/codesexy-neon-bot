import os
import requests
import schedule
import time
from datetime import datetime
from telegram import Bot

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL = '@CodeSexy2025'
bot = Bot(token=TOKEN)

def price(coin):
    try:
        return requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd').json()[coin]['usd']
    except:
        return {'bitcoin':103926, 'ethereum':3412, 'solana':182.5}.get(coin, 0)

def signal():
    b,e,s = price('bitcoin'), price('ethereum'), price('solana')
    return f"""NEON SİNYAL {datetime.now().strftime('%H:%M')}

BTC SHORT @ {b}$
TP1: {b-700}$ | SL: {b+500}$

ETH LONG @ {e}$
TP1: {e+100}$ | SL: {e-90}$

SOL SHORT @ {s}$
TP: {s-3}$ | SL: {s+2}$

#CodeSexy"""

schedule.every().day.at("09:00").do(lambda: bot.send_message(CHANNEL, signal()))
schedule.every().day.at("18:00").do(lambda: bot.send_message(CHANNEL, signal()))

while True:
    schedule.run_pending()
    time.sleep(60)
