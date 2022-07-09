# Import
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# Navegar whatsapp web
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://web.whatsapp.com/')
time.sleep(30)

# Definir mensagem e contato
contatos = ['something']
mensagem = ['oi', 'tudo bem?', 'até mais']

# Buscar o contato
def buscar_contato(contato):
    campo_de_pesquisa = driver.find_element_by_xpath('//div[contains(@class, "copyable-text selectable-text")]')
    time.sleep(3)
    campo_de_pesquisa.click()
    campo_de_pesquisa.send_keys(contato)
    campo_de_pesquisa.send_keys(Keys.ENTER)

# Enviar mensagem
def enviar_mensagem(mensagem):
    campo_de_mensagem = driver.find_elements_by_xpath('//div[contains(@class, "copyable-text selectable-text")]')
    campo_de_mensagem[1].click()
    time.sleep(3)
    for item in mensagem:
      campo_de_mensagem[1].send_keys(item)
      campo_de_mensagem[1].send_keys(Keys.ENTER)

# Rodar a lista de contatos
for contato in contatos:
    buscar_contato(contato)
    enviar_mensagem(mensagem)

