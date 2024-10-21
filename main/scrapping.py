from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time
import json
import datetime

# configurações do programa
options = Options()
# define se é para mostrar a janela ou não
#options.add_argument('--headless')
options.binary_location = r'C://Program Files//Mozilla Firefox//firefox.exe'
service = Service(r'.//driver//geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)
driver.get("https://br.indeed.com/")

dados = {}

def esperar_carregamento():
    time.sleep(4)

def busca_trabalho_e_local():
    esperar_carregamento()

    keyword_input = driver.find_element(By.ID, 'text-input-what')
    region_input = driver.find_element(By.ID, 'text-input-where')

    keyword_input.clear()
    region_input.clear()

    keyword_input.send_keys("Data Scientist")
    region_input.send_keys("São Paulo, SP")

    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
    submit_button.click()

def pega_dados():
    esperar_carregamento()

    

    cards = driver.find_elements(By.CSS_SELECTOR, 'div.job_seen_beacon')

    for card in cards:
        title = card.find_element(By.CSS_SELECTOR, 'h2 > a > span').get_attribute('title')
        company = card.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]').text
        location = card.find_element(By.CSS_SELECTOR, '[data-testid="text-location"]').text

        try:
            rating = card.find_element(By.CSS_SELECTOR, 'span[data-testid="holistic-rating"] > span[aria-hidden="true"]').text
        except:
            rating = "Nao informado"
        try:
            obs = card.find_element(By.CSS_SELECTOR,'div[data-testid="attribute_snippet_testid"]').text
        except:
            obs = "Nao informado"

        print(title, company, rating, location, obs, sep=" | ")

        dados.setdefault('title', []).append(title)
        dados.setdefault('company', []).append(company)
        dados.setdefault('rating', []).append(rating)
        dados.setdefault('location', []).append(location)
        dados.setdefault('obs', []).append(obs)


        with open('.//arquivosGerados//8_vagasIndeed.json', 'w') as f:
            json.dump(dados, f, indent=4)

    print("Dados salvos em vagasIndeed.json")

def passa_pagina():
    esperar_carregamento()
    button_next = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
    button_next.click()

def aceita_cookie():
    esperar_carregamento()
    try:
        button_cookie = driver.find_element(By.CSS_SELECTOR, 'button[id="onetrust-accept-btn-handler"]')
        button_cookie.click()
    except:
        pass

def fecha_popUP():
    esperar_carregamento()
    try:
        button_close = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="fechar"]')
        button_close.click()
    except:
        pass

def executar_scrapping():
    busca_trabalho_e_local()
    aceita_cookie()
    for i in range(0, 3):
        pega_dados()
        
        passa_pagina()

        fecha_popUP()

        
        

    esperar_carregamento()
    driver.quit()
'''


busca_trabalho_e_local()
aceita_cookie()
for i in range(0, 3):
    pega_dados()
    passa_pagina()
    fecha_popUP()

esperar_carregamento()
driver.quit()

'''
