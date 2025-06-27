from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC # Condições esperadas
from selenium.webdriver.support.ui import WebDriverWait # Para esperas explícitas
from selenium.webdriver.common.by import By # Para usar By.ID, By.CSS_SELECTOR etc.
import pandas as pd
import os

# abrir o navegador
navegador = webdriver.Chrome()

# deixar o navegador em tela cheia
navegador.maximize_window()

# acessar o site de salários do glassdoor
navegador.get("https://www.glassdoor.com.br/salaries/index.htm")

# encontrar o campo de pesquisa
campo_pesquisa = navegador.find_element("id", "job-title-autocomplete")

cargo = "Business Analytics"

# digitar no campo
campo_pesquisa.send_keys(cargo)

# encontrar botão de pesquisa
botao_buscar = navegador.find_element("class name", "HeroSearch_searchButton__33N2u")

# esperar
espera3 = WebDriverWait(navegador, 3)
espera10 = WebDriverWait(navegador, 10)

espera3.until(EC.element_to_be_clickable(botao_buscar)) 

# clicar no botão de pesquisa
botao_buscar.click()

# esperar até que o elemento do salário médio esteja presente
espera10.until(EC.presence_of_element_located((By.CLASS_NAME, "TotalPayRange_StyledAverageComp__m_S07")))
salario_medio = navegador.find_element("class name", "TotalPayRange_StyledAverageComp__m_S07")

# encontrar o elemento do salário médio
salario_texto = salario_medio.text
salario_limpo = salario_texto.replace("R$", "").replace(".", "").replace(" mil", "000").replace("- ", "-").strip()

# registrar salario no terminal
print(f"Salário médio para {cargo}: {salario_limpo}")

# criar uma lista para armazenar os dados
dados_cargos = []
dados_cargos.append({
    'Cargo (Glassdoor)': cargo,
    'Salário Médio' : salario_limpo,
    'Data coleta' : pd.Timestamp.now().strftime('%Y-%m-%d')
})

# armazenar os dados em um dataframe
df_salarios = pd.DataFrame(dados_cargos)

# consultar o excel já existente
df_existente = pd.read_excel("C:/Users/heros.dinao/Documents/automacoes/selenium/salarios/base_salarios.xlsx")
df_final = pd.concat([df_existente, df_salarios], ignore_index=True)

df_final.to_excel("C:/Users/heros.dinao/Documents/automacoes/selenium/salarios/base_salarios.xlsx", index=False)

time.sleep(10)