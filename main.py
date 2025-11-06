import os
import requests
import schedule
import time
from datetime import datetime
from telegram import Bot

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = '@CodeSexy2025'
bot = Bot(token=TELEGRAM_TOKEN)

def get_price(coin):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'
    try:
        return requests.get(url).json()[coin]['usd']
    except:
        return 0

def send_signal():
    btc = get_price('bitcoin') or 103926
    eth = get_price('ethereum') or 3412
    sol = get_price('solana') or 182.5

    msg = f"""⚡️ NEON SİNYAL {datetime.now().strftime('%H:%M')}

📉 BTC SHORT @ {btc}$
✅ TP1: {btc-700}$ | SL: {btc+500}$

📈 ETH LONG @ {eth}$
✅ TP1: {eth+100}$ | SL: {eth-90}$

📉 SOL SHORT @ {sol}$
✅ TP: {sol-3}$ | SL: {sol+2}$

#CodeSexy"""
    bot.send_message(chat_id=CHANNEL_ID, text=msg)

schedule.every().day.at("09:00").do(send_signal)
schedule.every().day.at("18:00").do(send_signal)

while True:
    schedule.run_pending()
    time.sleep(60)
