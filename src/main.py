import asyncio
import json
from datetime import datetime
from models import IndicatorDTO, PivotDTO, financialDTO
from playwright.async_api import async_playwright, Page
import re


def to_float(value: str) -> float | None:
    if value == "—":
        return None
    value = value.replace(".", "").replace(",", ".").strip().replace("−", "-")
    return float(value)


async def fetch_pivots(page, css_selector, interval, pair) -> list[PivotDTO]:
    await page.wait_for_selector(css_selector)

    elements = await page.locator(css_selector).all()
    pivot_list = []

    for i in range(0, len(elements), 6):
        pivot_list.append(
            PivotDTO(
                pair=pair,
                interval=interval,
                register_time=datetime.now().strftime("%d/%m/%Y %H:%M"),
                pivot=await elements[i].text_content(),
                classic=to_float(await elements[i + 1].text_content()),
                fibo=to_float(await elements[i + 2].text_content()),
                camarilla=to_float(await elements[i + 3].text_content()),
                woodie=to_float(await elements[i + 4].text_content()),
                dm=to_float(await elements[i + 5].text_content()),
            )
        )
    return pivot_list


async def fetch_indicators(page, css_selector, interval, pair) -> list[IndicatorDTO]:
    await page.wait_for_selector(css_selector)

    elements = await page.locator(css_selector).all()
    indicator_list = []

    for i in range(0, len(elements), 3):
        indicator_list.append(
            IndicatorDTO(
                pair=pair,
                interval=interval,
                register_time=datetime.now().strftime("%d/%m/%Y %H:%M"),
                name=await elements[i].text_content(),
                value=to_float(await elements[i + 1].text_content()),
                action=await elements[i + 2].text_content(),
            )
        )
    return indicator_list


async def fetch_price(page: Page) -> float:
    seletor = ".lastContainer-zoF9r75I"
    await page.wait_for_selector(seletor)
    element = page.locator(seletor).first
    price = await element.text_content()

    if price is not None:
        price_clean = re.sub(r"\D", "", price)
    return float(price_clean)


async def scrape_pair(pair: str, page: Page):
    url = f"https://tradingview.com/symbols/{pair}/technicals/"

    await page.goto(url, wait_until="domcontentloaded")

    oscillator_selector = "div:nth-child(1)> div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > *"
    moving_avg_selector = "div.container-hvDpy38G.maTable-kg4MJrFB.tableWithAction-kg4MJrFB.tabletVertical-kg4MJrFB.tabletVertical-hvDpy38G > div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > td"
    pivot_selector = "div.container-hvDpy38G.tabletVertical-hvDpy38G > div.container-Tv7LSjUz > div.wrapper-Tv7LSjUz > div > table > tbody > tr.row-hvDpy38G > td"

    intervals = ["1m"]  # "5m", "15m", "30m", "1h", "2h", "4h", "1D", "1W", "1M"]
    for interval in intervals:
        await page.wait_for_selector(f'button[id="{interval}"]')
        await page.click(f'button[id="{interval}"]', timeout=300)

        price = await fetch_price(page)
        oscillators = await fetch_indicators(page, oscillator_selector, interval, pair)
        moving_averages = await fetch_indicators(
            page, moving_avg_selector, interval, pair
        )
        pivots = await fetch_pivots(page, pivot_selector, interval, pair)

        asset = financialDTO(
            pair=pair,
            price=price,
            oscillators=oscillators,
            moving_averages=moving_averages,
            pivots=pivots,
        )
        print(f"Asset: {asset}")
        print("--" * 20 + "\n")


async def main():
    with open("pairs.json") as f:
        pairs = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        for pair in pairs:
            await scrape_pair(pair, page)


if __name__ == "__main__":
    asyncio.run(main())
