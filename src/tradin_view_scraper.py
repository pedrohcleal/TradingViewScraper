from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from config.chrome_config import create_driver
from selenium.webdriver.common.by import By
import json
from time import sleep
from pydantic import BaseModel
from pprint import pprint

class indicadorDTO(BaseModel):
    nome: str
    valor: float | None
    acao: str | None

class pivoDTO(BaseModel):
    pivo: str
    classico: float | None
    fibo: float | None
    camarilla: float | None
    woodie: float | None
    dm: float | None

driver: WebDriver = create_driver()

pares: list[str] = json.loads(open('pares.json').read())
intervalos: list[str] = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1D', '1W', '1M']
table_osciladores = 'div:nth-child(1)> div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > *'
table_mm = 'div.container-hvDpy38G.maTable-kg4MJrFB.tableWithAction-kg4MJrFB.tabletVertical-kg4MJrFB.tabletVertical-hvDpy38G > div.tableWrapper-hvDpy38G > table > tbody > tr.row-hvDpy38G > td'
table_pivo = 'div.container-hvDpy38G.tabletVertical-hvDpy38G > div.container-Tv7LSjUz > div.wrapper-Tv7LSjUz > div > table > tbody > tr.row-hvDpy38G > td'
tables_seletors: list[str] = [table_osciladores, table_mm, table_pivo]

def fetch_pivos(driver) -> list[pivoDTO]:
    pivos_elemento: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, table_pivo)
    lista_pivos: list[pivoDTO] = []
    for index in range(0, len([x for x in pivos_elemento]),6):
        lista_pivos.append(pivoDTO(
            pivo=pivos_elemento[index].text,
            classico=to_float(pivos_elemento[index+1].text),
            fibo=to_float(pivos_elemento[index+2].text),
            camarilla=to_float(pivos_elemento[index+3].text),
            woodie=to_float(pivos_elemento[index+4].text),
            dm=to_float(pivos_elemento[index+5].text)
            ))
    return lista_pivos
        
def fetch_medias_moveis(driver) -> list[indicadorDTO]:
    mms: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, table_mm)
    lista_mms: list[indicadorDTO] = []
    for index in range(0, len([x for x in mms]),3):
        lista_mms.append(indicadorDTO(
            nome=mms[index].text,
            valor=to_float(mms[index+1].text),
            acao=mms[index+2].text
            ))
    return lista_mms

def fetch_osciladores(driver) -> list[indicadorDTO]:
    indicators: list[WebElement] = driver.find_elements(By.CSS_SELECTOR, table_osciladores)
    lista_osciladores: list[indicadorDTO] = []
    for index in range(0,len([x for x in indicators]),3):
        lista_osciladores.append(indicadorDTO(
            nome=indicators[index].text,
            valor=to_float(indicators[index+1].text),
            acao=indicators[index+2].text
            ))
    return lista_osciladores

def to_float(strn: str) -> float | None:
    if strn == "—":
        return None
    while strn.count('.') > 1:
        strn = strn.replace('.', '', 1)
    strn = strn.strip().replace('−','-')
    converted = float(strn)
    return converted

def scraper(par) -> None:
    url: str = f'https://br.tradingview.com/symbols/{par}/technicals/'
    driver.get(url=url)
    sleep(1)
    for i in intervalos:
        bttn: WebElement = driver.find_element(By.ID, i)
        bttn.click()
        osciladores: list[indicadorDTO] = fetch_osciladores(driver=driver)
        medias: list[indicadorDTO] = fetch_medias_moveis(driver=driver)
        pivos: list[pivoDTO] = fetch_pivos(driver=driver)            
        print(f' INTERVALO = {i}')
        pprint(osciladores)
        pprint(medias)
        pprint(pivos)        
        print()
        
def main() -> None:
    for par in pares:
        scraper(par)
        

if __name__ == '__main__':
    main()