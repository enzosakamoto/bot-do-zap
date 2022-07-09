from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg

# Layout
sg.theme('GreenMono')
layout = [
    [sg.Push(), sg.Text('Bot para enviar mensagem para contatos no WhatsApp'), sg.Push()],
    [sg.Text('Digite o nome do contato: '), sg.Input(key = '-contato-', size = (40, 1)), sg.Button('Adicionar')],
    [sg.Text('Digite a mensagem: '), sg.Input(key = '-mensagem-'), sg.Button('Adicionar!')],
    [sg.Text('Quantas mensagens deseja enviar [cada]: '), sg.Input(key = '-numero-', size = (27,1)), sg.Button('Adicionar.')],
    [sg.Push(), sg.Output(key = 'linhas', size = (60,10)), sg.Push()],
    [sg.Push(), sg.Button('Enviar'), sg.Button('Limpar tudo!'), sg.Button('Sair'), sg.Push()],
    [sg.Push(), sg.Text('Versão 1.1 [beta]')]
]

# Janela
janela = sg.Window('Bot do zap', layout)

# Eventos
contatos = []
mensagens = []
quantidade_mensagem = 0

while True:
    eventos, valores = janela.read()

    def exibir_valores(contatos, mensagens, quantidade):
        print('Contatos adicionados:')
        print(contatos)
        print()
        print('Mensagens adicionadas:')
        print(mensagens)
        print()
        print('Mensagens a serem enviadas [para cada mensagem adicionada]:')
        print(quantidade)

    if eventos in (sg.WIN_CLOSED, 'Sair'):
        break

    if eventos == 'Limpar tudo!':
        janela['-contato-'].update('')
        janela['-mensagem-'].update('')
        janela['linhas'].update('')
        contatos = []
        mensagens = []

    if eventos == 'Adicionar':
        contatos.append(valores['-contato-'])
        janela['-contato-'].update('')
        janela['linhas'].update('')
        exibir_valores(contatos, mensagens, quantidade_mensagem)

    if eventos == 'Adicionar!':
        mensagens.append(valores['-mensagem-'])
        janela['-mensagem-'].update('')
        janela['linhas'].update('')
        exibir_valores(contatos, mensagens, quantidade_mensagem)

    if eventos == 'Adicionar.':
        quantidade_mensagem = int(valores['-numero-'])
        janela['-numero-'].update('')
        janela['linhas'].update('')
        exibir_valores(contatos, mensagens, quantidade_mensagem)

    if eventos == 'Enviar':
        janela.hide()

        # Navegar whatsapp web
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        time.sleep(30)
        

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
                for e in range(quantidade_mensagem):
                    campo_de_mensagem[1].send_keys(item)
                    campo_de_mensagem[1].send_keys(Keys.ENTER)

        # Rodar a lista de contatos
        for contato in contatos:
            buscar_contato(contato)
            enviar_mensagem(mensagens)

        break

janela.close()

