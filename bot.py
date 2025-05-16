import asyncio
from playwright.async_api import async_playwright
import requests
import os

# Variables d'environnement Railway
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MATCH_URL = "https://tickets.rafc.be/fr-FR/events"

async def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erreur envoi Telegram:", e)

async def check_seats():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(MATCH_URL)
        await page.wait_for_timeout(5000)

        content = await page.content()
        if "Antwerp - Union SG" in content:
            await send_telegram_alert("🚨 2 places peut-être dispos pour Antwerp - Union SG ! Va checker : https://tickets.rafc.be")
        else:
            print("Pas encore dispo...")

        await browser.close()

async def main():
    while True:
        try:
            await check_seats()
        except Exception as e:
            print("Erreur :", e)
        await asyncio.sleep(300)

asyncio.run(main())
