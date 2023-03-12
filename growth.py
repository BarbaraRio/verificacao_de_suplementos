import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_remetente = 'remetente@yahoo.com' 
senha_remetente = 'senha-do-remetente'
email_destinatario1 = 'destinatario1@gmail.com'
email_destinatario2 = 'destinatario2@hotmail.com'

def verifica_sabores():

    disponibilidade_de_sabores = {
        "Morango": False,
        "Cookies": False
    }
    
    url = 'https://gsuplementos.com.br'
    driver = webdriver.Chrome() #(executable_path=caminho_executavel_chromedriver, options=chrome_options)
    driver.get(url)
    driver.maximize_window()

    #buscando o produto
    caixa_de_busca = driver.find_element(by=By.XPATH, value='//*[@id="busca"]/input')
    caixa_de_busca.click()
    caixa_de_busca.send_keys('whey concentrado')
    confirmar = driver.find_element(by=By.XPATH, value='//*[@id="busca"]/button/img')
    confirmar.click()
    time.sleep(1)
    driver.execute_script('window.scrollBy(0, 250);')
    whey_concentrado = driver.find_element(by=By.XPATH, value='/html/body/main/article/section[5]/div/div[2]/div[2]/div/div/div[1]/div[2]/a/h3')
    whey_concentrado.click()

    #selecionando o sabor
    driver.execute_script('window.scrollBy(0, 400);')
    escolha_sabor = driver.find_element(by=By.XPATH, value='/html/body/main/section[3]/div[1]/div[3]/div/div[2]/div[1]/div')
    escolha_sabor.click()
    contador = 2
    while True:
        try:
            sabor = driver.find_element(by=By.XPATH, value=f'/html/body/main/section[3]/div[1]/div[3]/div/div[2]/div[1]/div/ul/li[{contador}]')
            if sabor.get_attribute("class") == "option" and sabor.get_attribute("data-value") == '2':
                disponibilidade_de_sabores['Morango'] = True
            if sabor.get_attribute("class") == "option" and sabor.get_attribute("data-value") == '26':
                disponibilidade_de_sabores['Cookies'] = True
        except:
            break
        contador += 1

    driver.quit()

    return disponibilidade_de_sabores

def envia_email(sabores_disponiveis):
    smtp_servidor = 'smtp.gmail.com'
    smtp_port = 587
    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = ', '.join([email_destinatario1, email_destinatario2])
    mensagem['Subject'] = 'Novidade na GROWTH'

    texto_base = "Disponivel agora:\n"
    terceira_parte = f" e {sabores_disponiveis[-1]}"

    if len(sabores_disponiveis) < 2:
        segunda_parte = sabores_disponiveis[0]
        texto_da_mensagem = texto_base + segunda_parte
    elif len(sabores_disponiveis) >= 2:
        segunda_parte = ", ".join(sabores_disponiveis[:-1])
        texto_da_mensagem = texto_base + segunda_parte + terceira_parte

    mensagem.attach(MIMEText(texto_da_mensagem, 'plain'))
    sessao = smtplib.SMTP(smtp_servidor, smtp_port)
    sessao.starttls()
    sessao.login(email_remetente, senha_remetente)
    sessao.send_message(mensagem)
    sessao.quit()

def main():
    sabores_disponiveis = []
    sabores = verifica_sabores()
    for sabor in sabores:
        if sabores[sabor]:
            sabores_disponiveis.append(sabor)
    
    if len(sabores_disponiveis) > 0:
        envia_email(sabores_disponiveis)

if __name__ == '__main__':
    main()


