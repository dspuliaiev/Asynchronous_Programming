import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_currency_rates(days):
    url = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"
    currency_codes = ["EUR", "USD"]
    result = []

    async with aiohttp.ClientSession() as session:
        for day in range(days):
            date = (datetime.now() - timedelta(days=day)).strftime("%d.%m.%Y")
            async with session.get(url.format(date)) as response:
                data = await response.json()
                rates = {code: {"sale": None, "purchase": None} for code in currency_codes}
                for rate in data["exchangeRate"]:
                    if rate["currency"] in currency_codes:
                        rates[rate["currency"]]["sale"] = rate["saleRateNB"]
                        rates[rate["currency"]]["purchase"] = rate["purchaseRateNB"]
                result.append({date: rates})

    return result

if __name__ == "__main__":
    try:
        days = int(sys.argv[1])
        loop = asyncio.get_event_loop()
        currency_rates = loop.run_until_complete(fetch_currency_rates(days))
        print(currency_rates)
    except (ValueError, IndexError):
        print("Usage: py .\\main.py <number_of_days>")