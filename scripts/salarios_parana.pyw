from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC # Condições esperadas
from selenium.webdriver.support.ui import WebDriverWait # Para esperas explícitas
from selenium.webdriver.common.by import By # Para usar By.ID, By.CSS_SELECTOR etc.
from selenium.webdriver.common.keys import Keys # Para usar ARROW_DOWN e ENTER
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import datetime

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Define o caminho da planilha de cargos e do arquivo de saída
CAMINHO_PLANILHA_CARGOS = os.path.join(os.path.dirname(os.getcwd()), "Cargos.xlsx")
NOME_ARQUIVO_SAIDA_EXCEL = "base_salarios_glassdoor.xlsx" # Nome do arquivo onde os salários serão salvos
CAMINHO_ARQUIVO_SAIDA_EXCEL = os.path.join(os.path.dirname(os.getcwd()), NOME_ARQUIVO_SAIDA_EXCEL)
CAMINHO_LOGS = os.path.join(os.getcwd(), "logs")

# Gera o nome do arquivo de log com a data e hora atuais
nome_arquivo_log = datetime.datetime.now().strftime("log_%d-%m-%Y_%H-%M.txt")
caminho_arquivo_log = os.path.join(CAMINHO_LOGS, nome_arquivo_log)

# Abre o arquivo de log para escrita 
log_file = open(caminho_arquivo_log, 'w', encoding='utf-8')

# Função auxiliar para imprimir no console E no arquivo de log
def log_print(message):
    print(message) # Usa a função 'print' embutida do Python
    log_file.write(message + "\n") # Escreve no arquivo de log

# --- VARIÁVEIS PARA O LOG DE EXECUÇÃO ---
horario_inicio_script = datetime.datetime.now()
salarios_encontrados_contador = 0
salarios_nao_encontrados_contador = 0

# Lista para armazenar todos os dados coletados antes de salvar no Excel
todos_dados_cargos = []

log_print(f"--- INÍCIO DA EXECUÇÃO DO SCRIPT DE COLETA DE SALÁRIOS ---")
log_print(f"Horário de Início: {horario_inicio_script.strftime('%d/%m/%Y %H:%M:%S')}")

# Abre o navegador
log_print("Iniciando navegador Chrome...")
try:
    navegador = webdriver.Chrome(options=chrome_options)
    log_print("Navegador Chrome iniciado com sucesso.")
except Exception as e:
    log_print(f"ERRO: Não foi possível iniciar o navegador Chrome. Verifique o ChromeDriver e as opções. Erro: {e}")
    log_file.close() # Garante que o log seja salvo mesmo em caso de erro crítico no início
    exit()

# --- Carregar a lista de cargos da planilha base ---
try:
    df_cargos = pd.read_excel(CAMINHO_PLANILHA_CARGOS)
    lista_de_cargos = df_cargos['Cargo'].tolist()
    log_print(f"Número de cargos a serem pesquisados: {len(lista_de_cargos)}")
except FileNotFoundError:
    log_print(f"ERRO: A planilha de cargos não foi encontrada em '{CAMINHO_PLANILHA_CARGOS}'. Por favor, verifique o caminho.")
    navegador.quit()
    log_file.close()
    exit()
except KeyError:
    log_print(f"ERRO: A coluna 'Cargo' não foi encontrada em '{CAMINHO_PLANILHA_CARGOS}'. Verifique o nome da coluna.")
    navegador.quit()
    log_file.close()
    exit()

# Limpa o arquivo de saída antes de iniciar a automação
colunas_saida = ['Cargo Pesquisado', 'Cargo no Glassdoor', 'Salário Médio Glassdoor', 'Data Coleta']
df_vazio = pd.DataFrame(columns=colunas_saida)
df_vazio.to_excel(CAMINHO_ARQUIVO_SAIDA_EXCEL, index=False)

# --- Loop para cada cargo ---
for cargo_para_pesquisar in lista_de_cargos:
    log_print(f"\n--- Pesquisando salário para: {cargo_para_pesquisar} ---")

    try:
        # Acessar a página de salários do Glassdoor no início de cada iteração
        navegador.get("https://www.glassdoor.com.br/salaries/index.htm")

        # Encontrar o campo de pesquisa (usando ID)
        campo_pesquisa = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, "job-title-autocomplete"))
        )

        # Limpar o campo antes de digitar o novo cargo
        campo_pesquisa.clear()

        # Digitar o cargo no campo
        campo_pesquisa.send_keys(cargo_para_pesquisar)
        time.sleep(1)
        
        # Digitar PR como localização
        campo_localizacao = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, "location-autocomplete")))
        campo_localizacao.clear()
        campo_localizacao.send_keys("PR (Brasil)")
        time.sleep(2)
        campo_localizacao.send_keys(Keys.ARROW_DOWN)
        campo_localizacao.send_keys(Keys.ENTER)
        
        # Encontrar o botão de pesquisa
        botao_buscar = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "HeroSearch_searchButton__33N2u"))
        )
        botao_buscar.click()

        # Esperar até que o elemento do salário médio esteja presente na página de resultados
        salario_elemento = WebDriverWait(navegador, 12).until(
            EC.presence_of_element_located((By.CLASS_NAME, "TotalPayRange_StyledAverageComp__m_S07"))
        )
        salario_texto = salario_elemento.text

        try:
            nome_cargo_elemento_glassdoor = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[5]/main/section[1]/div[1]/div/span/h1/span[1]"))
            )
            nome_cargo_no_glassdoor = nome_cargo_elemento_glassdoor.text
        except Exception as nome_err:
            log_print(f"Aviso: Não foi possível capturar o nome exato do cargo do Glassdoor para '{cargo_para_pesquisar}'. Usando o nome pesquisado. Erro: {nome_err}")
        
        # Processar o texto do salário
        salario_limpo = salario_texto.replace("R$", "").replace(".", "").replace(" mil", "000").strip()
        log_print(f"Salário médio encontrado para {nome_cargo_no_glassdoor}: {salario_limpo}")

        # Adicionar os dados à lista
        todos_dados_cargos.append({
            'Cargo Pesquisado': cargo_para_pesquisar,
            'Cargo no Glassdoor': nome_cargo_no_glassdoor,
            'Salário Médio Glassdoor': salario_limpo, # Mantendo como string para preservar a faixa se houver
            'Data Coleta': pd.Timestamp.now().strftime('%Y-%m-%d')
        })
        salarios_encontrados_contador += 1
        
    except Exception as e:
        log_print(f"Não foi possível obter o salário para '{cargo_para_pesquisar}'. Erro: {e}")
        salarios_nao_encontrados_contador += 1
        
        # Se um cargo não for encontrado ou der erro, ainda assim adicionamos para registro
        todos_dados_cargos.append({
            'Cargo Pesquisado': cargo_para_pesquisar,
            'Cargo no Glassdoor': 'Não encontrado',
            'Salário Médio Glassdoor': 'Não encontrado',
            'Data Coleta': pd.Timestamp.now().strftime('%Y-%m-%d')
        })
# --- Finalizar: Salvar todos os dados coletados no Excel ---
log_print("\n--- Salvando dados no Excel ---")
if todos_dados_cargos:
    df_novos_salarios = pd.DataFrame(todos_dados_cargos)

    # Verificar se o arquivo de saída já existe
    if os.path.exists(CAMINHO_ARQUIVO_SAIDA_EXCEL):
        try:
            df_existente = pd.read_excel(CAMINHO_ARQUIVO_SAIDA_EXCEL)
            # Concatena os dados existentes com os novos
            df_final = pd.concat([df_existente, df_novos_salarios], ignore_index=True)
            # Remove duplicatas para o mesmo cargo na mesma data, mantendo a última entrada
            df_final.drop_duplicates(subset=['Cargo Pesquisado', 'Data Coleta'], keep='last', inplace=True)
            log_print(f"Dados adicionados e atualizados no arquivo existente: {NOME_ARQUIVO_SAIDA_EXCEL}")
        except Exception as e:
            log_print(f"Atenção: Erro ao ler o arquivo Excel existente ({e}). Criando um novo com os dados coletados.")
            df_final = df_novos_salarios # Se houver erro na leitura do existente, cria um novo
    else:
        df_final = df_novos_salarios # Se o arquivo não existe, o final é apenas os novos dados
        log_print(f"Arquivo Excel não encontrado. Será criado um novo em: {CAMINHO_ARQUIVO_SAIDA_EXCEL}")

    # Tenta salvar o DataFrame final no Excel
    try:
        df_final.to_excel(CAMINHO_ARQUIVO_SAIDA_EXCEL, index=False)
        log_print("Dados salvos no Excel com sucesso!")
    except PermissionError:
        log_print(f"ERRO: O arquivo Excel '{NOME_ARQUIVO_SAIDA_EXCEL}' está aberto ou bloqueado. Por favor, feche-o e tente novamente.")
    except Exception as e:
        log_print(f"ERRO inesperado ao salvar o arquivo Excel: {e}")
else:
    log_print("Nenhum dado de salário foi coletado para salvar.")

# Fechar o navegador no final
navegador.quit()
log_print("Script finalizado.")

# --- LOG FINAL DE EXECUÇÃO ---
horario_termino_script = datetime.datetime.now()
tempo_total_execucao = horario_termino_script - horario_inicio_script

log_print("\n--- RESUMO DA EXECUÇÃO DO SCRIPT ---")
log_print(f"Horário de Início: {horario_inicio_script.strftime('%d/%m/%Y %H:%M:%S')}")
log_print(f"Horário de Término: {horario_termino_script.strftime('%d/%m/%Y %H:%M:%S')}")
log_print(f"Tempo Total de Execução: {tempo_total_execucao}")
log_print(f"Total de Cargos Pesquisados: {len(lista_de_cargos)}")
log_print(f"Salários Encontrados com Sucesso: {salarios_encontrados_contador}")
log_print(f"Salários Não Encontrados/Com Erro: {salarios_nao_encontrados_contador}")
log_print("------------------------------------")
log_print("Script concluído. Verifique o arquivo Excel e o arquivo de Log para os resultados.")

log_file.close() # Garante que o arquivo de log seja fechado ao final do script