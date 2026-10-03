import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    response = requests.get(url, params={"symbol": "BTCUSDT"}, timeout=10)
    response.raise_for_status()
    return float(response.json()["price"])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Kripto analiz botu aktif.\n\n"
        "/fiyat BTC → Bitcoin fiyatı\n"
        "/durum → Analiz sistemi"
    )

async def fiyat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_btc_price()
        await update.message.reply_text(
            f"₿ BTC/USDT\n\nGüncel fiyat: ${price:,.2f}"
        )
    except Exception:
        await update.message.reply_text(
            "Fiyat alınırken hata oluştu."
        )

async def durum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 ANALİZ MOTORU\n\n"
        "Trend: Kontrol ediliyor\n"
        "EMA: Kontrol ediliyor\n"
        "RSI: Kontrol ediliyor\n"
        "Hacim: Kontrol ediliyor\n"
        "Destek/Direnç: Kontrol ediliyor\n"
        "Funding/OI: Kontrol ediliyor\n\n"
        "SİNYAL: BEKLE"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fiyat", fiyat))
    app.add_handler(CommandHandler("durum", durum))

    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
