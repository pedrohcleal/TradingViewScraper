from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_config import create_driver
import json
from pprint import pprint
from datetime import datetime
from models import IndicatorDTO, PivotDTO


driver: WebDriver = create_driver()
pairs: list[str] = json.loads(open("pairs.json").read())
intervals: list[str] = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1D", "1W", "1M"]
oscillator_table = (
    "div:nth-child(1)> div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > *"
)
moving_average_table = "div.container-hvDpy38G.maTable-kg4MJrFB.tableWithAction-kg4MJrFB.tabletVertical-kg4MJrFB.tabletVertical-hvDpy38G > div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > td"
pivot_table = "div.container-hvDpy38G.tabletVertical-hvDpy38G > div.container-Tv7LSjUz > div.wrapper-Tv7LSjUz > div > table > tbody > tr.row-hvDpy38G > td"


def fetch_pivots(driver: WebDriver, interval, pair) -> list[PivotDTO]:
    pivot_elements: list[WebElement] = driver.find_elements(
        By.CSS_SELECTOR, pivot_table
    )
    pivot_list: list[PivotDTO] = []
    for index in range(0, len(pivot_elements), 6):
        pivot_list.append(
            PivotDTO(
                pair=pair,
                interval=interval,
                register_time=datetime.now().strftime("%d/%m/%Y %H:%M"),
                pivot=pivot_elements[index].text,
                classic=to_float(pivot_elements[index + 1].text),
                fibo=to_float(pivot_elements[index + 2].text),
                camarilla=to_float(pivot_elements[index + 3].text),
                woodie=to_float(pivot_elements[index + 4].text),
                dm=to_float(pivot_elements[index + 5].text),
            )
        )
    return pivot_list


def fetch_indicators(
    driver: WebDriver, css_selector, interval, pair
) -> list[IndicatorDTO]:
    oscillator_elements: list[WebElement] = driver.find_elements(
        By.CSS_SELECTOR, oscillator_table
    )
    oscillator_list: list[IndicatorDTO] = []
    for index in range(0, len(oscillator_elements), 3):
        oscillator_list.append(
            IndicatorDTO(
                pair=pair,
                interval=interval,
                register_time=datetime.now().strftime("%d/%m/%Y %H:%M"),
                name=oscillator_elements[index].text,
                value=to_float(oscillator_elements[index + 1].text),
                action=oscillator_elements[index + 2].text,
            )
        )
    return oscillator_list


def to_float(value: str) -> float | None:
    if value == "—":
        return None
    value = value.replace(".", "").replace(",", ".").strip().replace("−", "-")
    return float(value)


def scrape_pair(pair: str) -> None:
    url: str = f"https://tradingview.com/symbols/{pair}/technicals/"
    driver.get(url)
    for interval in intervals:
        interval_bttn: WebElement = WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_element_located((By.ID, interval))
        )
        interval_bttn.click()

        oscillators: list[IndicatorDTO] = fetch_indicators(
            driver, oscillator_table, interval, pair
        )

        moving_averages: list[IndicatorDTO] = fetch_indicators(
            driver, moving_average_table, interval, pair
        )

        pivots: list[PivotDTO] = fetch_pivots(driver, interval, pair)

        print(f"INTERVAL = {interval}, PAIR = {pair}")
        print("Oscillators:")
        pprint(oscillators)
        print("\nMoving Averages:")
        pprint(moving_averages)
        print("\nPivots:")
        pprint(pivots)
        print()

if __name__ == "__main__":
    for pair in pairs:
        scrape_pair(pair)
