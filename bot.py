import asyncio
from playwright.async_api import async_playwright
import requests
import os
TELEGRAM_BOT_TOKEN = os.environ["7713441397:AAE6YLp1nDx4wCWN2cGSrJW8sMI1bfGhmRg"]
TELEGRAM_CHAT_ID = os.environ["815969427"]

MATCH_URL = "https://tickets.rafc.be/fr-FR/events"

async def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

async def check_seats():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(MATCH_URL)

        await page.wait_for_timeout(5000)  # Laisse le site charger

        if "Antwerp - Union SG" in await page.content():
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
        await asyncio.sleep(300)  # 5 minutes

asyncio.run(main())
