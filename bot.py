import asyncio
from playwright.async_api import async_playwright
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MATCH_URL = "https://tickets.rafc.be/fr-FR/events/r-antwerp-fc-r-union-sg-champions-play-offs-/2025-05-17T20:45:00Z/tickets"

async def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=payload)
        print("Notification envoyée, statut :", r.status_code)
    except Exception as e:
        print("Erreur envoi Telegram:", e)

async def check_seats():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(MATCH_URL)

        try:
            await page.wait_for_selector("svg, .seat, .zone, .Section", timeout=10000)
        except:
            print("Plan non trouvé, peut-être plus de ventes ouvertes.")
            await browser.close()
            return

        content = await page.content()

        # Tentative de trouver des sièges disponibles
        seats = await page.query_selector_all("circle[class*=available], .seat.available, .zone.available")
        print(f"{len(seats)} place(s) détectée(s)")

        if len(seats) >= 2:
            await send_telegram_alert("🎟️ 2 places ou plus sont DISPONIBLES pour Antwerp - Union SG ! Vite sur : https://tickets.rafc.be")
        else:
            print("Pas encore 2 places côte à côte...")

        await browser.close()

async def main():
    while True:
        try:
            await check_seats()
        except Exception as e:
            print("Erreur dans le bot :", e)
        await asyncio.sleep(300)

asyncio.run(main())
