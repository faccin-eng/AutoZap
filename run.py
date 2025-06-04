import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Configurações do Chrome
options = Options()
options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
options.add_experimental_option("detach", True)  # Não fecha o navegador depois
options.add_argument('--user-data-dir=C:/temp/BraveProfile')
service = Service("chromedriver.exe")  # ou o caminho completo se não estiver no mesmo diretório
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com")

# Abre o WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Escaneie o QR Code e pressione Enter aqui...")

# Lê os contatos
df = pd.read_csv("contatos.csv", encoding="latin1")
df = df.rename(columns=lambda x: x.strip().replace(";", "").lower())  # padroniza nome da coluna
df = df.dropna()
numeros = df.iloc[:, 0].astype(str).str.strip()

# Mensagem que será enviada
mensagem = "Olá! Obrigado por participar da 1º Conferência.... por favor cique no link"

# Envia mensagens
for numero in numeros:
    try:
        numero = numero.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
        if not numero.startswith("+"):
            numero = "+55" + numero

        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
        driver.get(url)
        time.sleep(10)  # Tempo para carregar a conversa

        # Pressiona Enter para enviar
        caixa = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        caixa.send_keys(Keys.ENTER)

        print(f"Enviado para {numero}")
        time.sleep(10)  # Pausa entre envios

    except Exception as e:
        print(f"Erro com {numero}: {e}")
        continue
