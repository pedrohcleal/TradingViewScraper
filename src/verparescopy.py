from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from config.chrome_config import create_driver
from selenium.webdriver.common.by import By
import json
from time import sleep
from pydantic import BaseModel
from pprint import pprint

driver: WebDriver = create_driver()

   
def main() -> None:
    url: str = f'https://br.tradingview.com/ideas/pivotpoints/'
    driver.get(url=url)
    sleep(15)
    container = driver.find_elements(By.CSS_SELECTOR, '#overlap-manager-root > div:nth-child(2) > div > div.wrap-VeoIyDt4 > div > div > div.modal-mQsMiuFL.dialog-VeoIyDt4.dialog-aRAWUDhF.rounded-aRAWUDhF.shadowed-aRAWUDhF.fullscreen-aRAWUDhF > div > div.body-LflgdzFa > div > div.wrap-dlewR1s1 > div > div > *')
    for i in container:
        i.find_element(By.CSS_SELECTOR,'span')
        print(i.text)
        
if __name__ == '__main__':
    main()