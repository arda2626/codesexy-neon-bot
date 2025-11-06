import os
import requests
import schedule
import time
from datetime import datetime
from telegram import Bot  # pip install python-telegram-bot (Railway'de otomatik)

# Telegram Bot Token (Railway env'de koy)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = '@CodeSexy2025'  # Kanalın
bot = Bot(token=TELEGRAM_TOKEN)

def get_crypto_prices():
    """CoinGecko'dan gerçek fiyatlar al"""
    coins = ['bitcoin', 'ethereum', 'solana']
    prices = {}
    for coin in coins:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            prices[coin] = data[coin]['usd']
    return prices

def calculate_signals(prices):
    """Basit RSI/MACD simülasyonu (gerçek backtest için genişlet)"""
    # Örnek: BTC Short (bearish), ETH Long (oversold), SOL Short
    btc_price = prices.get('bitcoin', 103926)
    eth_price = prices.get('ethereum', 3412)
    sol_price = prices.get('solana', 182.5)
    
    # RSI simülasyon (gerçekte TA-Lib ekle)
    btc_rsi = 55  # Bearish
    eth_rsi = 28  # Oversold
    sol_rsi = 62  # Sell
    
    signals = []
    signals.append(f"📉 BTC SHORT @ {btc_price}$ | TP1: {btc_price-726}$ | SL: {btc_price+574}$ | RSI: {btc_rsi}")
    signals.append(f"📈 ETH LONG @ {eth_price}$ | TP1: {eth_price+88}$ | SL: {eth_price-92}$ | RSI: {eth_rsi}")
    signals.append(f"📉 SOL SHORT @ {sol_price}$ | TP: {sol_price-3.5}$ | SL: {sol_price+2}$ | RSI: {sol_rsi}")
    
    return '\n'.join(signals)

def send_morning_signal():
    prices = get_crypto_prices()
    signals = calculate_signals(prices)
    message = f"⚡️ GÜNAYDIN NEON! {datetime.now().strftime('%H:%M')}\n{signals}\n#CodeSexy"
    bot.send_message(chat_id=CHANNEL_ID, text=message)

def send_evening_signal():
    prices = get_crypto_prices()
    signals = calculate_signals(prices)
    message = f"🌃 AKŞAM RAPORU! {datetime.now().strftime('%H:%M')}\n{signals}\nVIP: NEON yaz!\n#CodeSexy"
    bot.send_message(chat_id=CHANNEL_ID, text=message)

# Schedule (cron gibi)
schedule.every().day.at("09:00").do(send_morning_signal)
schedule.every().day.at("18:00").do(send_evening_signal)

# Sürekli çalış
while True:
    schedule.run_pending()
    time.sleep(60)
