**Desafio Técnico de Web Scraping**

### Objetivo
Desenvolver um scraper em **Python** para coletar dados de livros disponíveis no site [Books to Scrape](https://books.toscrape.com/) utilizando **Selenium** ou **BeautifulSoup**.

O propósito do desafio é:
- Realizar scraping de múltiplas páginas.
- Validar os dados coletados com **Pydantic**.
- Exibir os dados em **DTOs** validados.
- Estruturar o projeto de forma organizada.
- Publicar o código em um repositório público no GitHub.

---

### **Requisitos do Projeto**

1. **Dados a serem extraídos de cada livro:**
   - Nome do livro.
   - Link da imagem da capa.
   - Preço do livro.
   - Quantidade de estrelas.
   - Disponibilidade em estoque (sim/não).

2. **Percorrer todas as páginas:**
   O scraper deve navegar por todas as páginas do site até coletar todos os dados.

3. **Validação dos dados com Pydantic:**
   - Crie uma classe DTO utilizando o Pydantic.
   - Valide cada livro coletado.

4. **Imprimir os DTOs validados:**
   Exiba os dados formatados no console.

5. **Uso de Selenium ou BeautifulSoup:**
   - Utilize **Selenium** como primeira opção (mais fácil, porém mais lento).
   - BeautifulSoup pode ser usado como alternativa.

6. **Publicar no GitHub:**
   - Estruture o código em um projeto organizado.
   - Crie um repositório público no GitHub com um README detalhado.

---

### Estrutura Sugerida do Projeto

```
books_scraper/
│
├── chrome_config.py       # Configuração padrão do ChromeDriver (fornecida abaixo)
├── dto.py                 # Definição do DTO com Pydantic
├── scraper.py             # Lógica principal do scraping
├── main.py                # Ponto de entrada do projeto
└── requirements.txt       # Dependências do projeto
```

---

### Configuração do Selenium
O arquivo `chrome_config.py` contém a configuração padrão para o **ChromeDriver** usando **webdriver_manager**. 

#### **chrome_config.py**
```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from contextlib import contextmanager


@contextmanager
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # comentar essa linha para ver as iterações no chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-animations")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-prefetch")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        yield driver
    finally:
        print('fim do chromedriver')
        driver.quit()
```

---

### Como Usar a Configuração

No seu arquivo `scraper.py`, importe a configuração acima e utilize o **context manager** para inicializar o ChromeDriver:

```python
from chrome_config import create_driver

with create_driver() as driver:
    driver.get("https://books.toscrape.com/")
    # Escreva aqui a lógica de scraping
```

---

### Passos Finais

1. **Instalar as dependências:**
   Utilize um arquivo `requirements.txt` para gerenciar as bibliotecas:

   ```txt
   selenium
   pydantic
   webdriver_manager
   beautifulsoup4  # Opcional, se utilizar BS4
   ```

2. **Executar o projeto localmente:**
   Certifique-se de que todas as dependências estejam instaladas:

   ```bash
   pip install -r requirements.txt
   python main.py
   ```

3. **Publicar no GitHub:**
   - Crie um repositório público.
   - Faça commit do projeto e adicione um README explicando o que o projeto faz e como rodar.

---

### Bônus
Adicione instruções no README sobre como instalar e rodar o projeto em qualquer ambiente.

Bom desafio! 🚀
