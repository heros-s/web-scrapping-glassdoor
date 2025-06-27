# Coletor de Salários Glassdoor - Média Salarial por Cargo (PR, Brasil)

Este documento serve como um guia completo para você utilizar o script Python de coleta de salários do Glassdoor. Ele foi projetado para automatizar a busca de salários médios de cargos específicos em **Paraná (PR), Brasil**, e registrar esses dados em um arquivo Excel, além de gerar logs detalhados da execução.

### O que o Script Faz?

O script irá:
* Abrir o navegador Google Chrome em um ambiente controlado (sem usar seu perfil principal para evitar conflitos).
* Para cada cargo listado em sua planilha de entrada:
    * Acessar a página de salários do Glassdoor.
    * Digitar o cargo no campo de pesquisa.
    * Digitar "PR (Brasil)" no campo de localização.
    * Clicar no botão de busca.
    * Extrair o salário médio exibido na página de resultados.
    * Registrar o nome do cargo (o nome exato do Glassdoor ou o original, se não encontrado), a localização, o salário médio e a data da coleta.
* Salvar (ou adicionar a) todos os dados coletados em um arquivo Excel de saída.
* Gerar um arquivo de log (`.txt`) com informações detalhadas da execução, incluindo horários e contagens.

---

## 👤 Autor

Desenvolvido por: **Heros Dinao**
* [LinkedIn](https://www.linkedin.com/in/heros-dinao)
* [GitHub](https://github.com/heros-s)
## Pré-requisitos
---

Para que o script funcione corretamente em qualquer máquina Windows, você precisará ter o seguinte:

* **Python:** É necessário ter o Python instalado em seu sistema (versão 3.6 ou superior é recomendada).
* **Google Chrome:** O navegador Google Chrome deve estar instalado e atualizado.
* **Bibliotecas Python:** As seguintes bibliotecas Python são usadas pelo script:
    * `selenium`: Para automação do navegador.
    * `pandas`: Para manipulação de dados e trabalho com arquivos Excel.
    * `openpyxl`: Uma dependência do Pandas para ler/escrever arquivos `.xlsx`.

    Para instalá-las (se ainda não as tiver), abra seu terminal (Prompt de Comando) e execute o seguinte comando:
    ```bash
    pip install selenium pandas openpyxl
    ```

* **Credenciais do Glassdoor:** O script está configurado para fazer login automaticamente. Você precisará garantir que seu e-mail e senha estejam corretos no código-fonte Python original (`salarios_parana.py`). **Por motivos de segurança, evite deixar credenciais hardcoded em sistemas de produção.**

---

## Configuração e Preparação

Antes de executar o script, siga estas etapas para configurá-lo corretamente:

1.  **Estrutura de Pastas:**
    Certifique-se de que a pasta (`1 - Web Scraping Glassdoor`) contenha os seguintes itens:
    * `Cargos.xlsx` (sua planilha de entrada)
    * `base_salarios_glassdoor.xlsx` (será criado ou atualizado nesta pasta)
    * `scripts` (pasta contendo os scripts .pyw, o .bat do script e uma subpasta de logs)
    * `1 - Média de salários Paraná.bat` (o arquivo .bat para execução da automação)
    * `salarios_parana.pyw` (o script da automação em .pyw)
    * Uma subpasta chamada `logs` (será criada automaticamente, mas é bom saber a localização)

2.  **Planilha de Cargos (`Cargos.xlsx`):**
    * Edite o arquivo Excel com o nome **`Cargos.xlsx`** (com 'C' maiúsculo e extensão `.xlsx`).
    * Dentro deste arquivo, na **primeira aba**, use a coluna chamada **"Cargo"** (com 'C' maiúsculo).
    * Nesta coluna, liste todos os cargos que você deseja pesquisar no Glassdoor, um por linha.
        Exemplo:
        ```
        Cargo
        -----------------------
        Business Analytics
        Analista de Cobrança
        Gerente Financeiro
        Auxiliar Administrativo
        ```

---

## Como Executar o Script

1.  **Feche todas as instâncias do Google Chrome!**
    * Isso é **fundamental**. Se o Chrome estiver aberto, o script não conseguirá iniciar no perfil correto.
    * Verifique também no Gerenciador de Tarefas (`Ctrl + Shift + Esc` no Windows) se não há processos `chrome.exe` ou `chromedriver.exe` rodando em segundo plano e finalize-os.

2.  **Verifique a `Cargos.xlsx`:**
    * Certifique-se de que sua planilha de cargos esteja na **pasta anterior** a do executável.

3.  **Edite o Arquivo `.bat`:**
    * Na pasta onde você tem o executável, haverá um arquivo chamado **`1 - Média de salários Paraná.bat`**.
    * Clique com o botão direito no arquivo `1 - Média de salários Paraná.bat` e selecione "Editar" (ou "Edit"). Ele será aberto em um editor de texto (como o Bloco de Notas).
    * O `.bat` tem uma linha como `"C:\Users\heros.dinao\AppData\Local\Microsoft\WindowsApps\python.exe"`
    * Altere este caminho (`"C:\Users\{seu.usuario}\AppData\Local\Microsoft\WindowsApps\python.exe"`) 
    * Altere o segundo diretório para onde você realmente colocou a pasta do script (`1 - Web Scraping Glassdoor`).
    * Salve o arquivo `.bat` (`Ctrl + S`).
    * Dê um duplo clique neste arquivo `.bat`.
    * Uma janela do Prompt de Comando (console) se abrirá, e o Google Chrome será iniciado e automatizado.

4.  **Monitore a Execução:**
    * A janela do console mostrará o progresso do script em tempo real.
    * Você verá o navegador Chrome abrindo e realizando as interações (login, digitação, busca).
    * Todas as mensagens exibidas no console também serão salvas no arquivo de log.
    * Você pode continuar seu trabalho enquanto a automação roda em segundo plano.

---

## Saídas do Script

Após a execução, você encontrará os seguintes arquivos e pastas gerados:

1.  **`base_salarios_glassdoor.xlsx`:**
    * Localizado na pasta anterior a do executável.
    * Este arquivo Excel conterá os salários médios coletados para cada cargo em Paraná (Brasil).
    * **Será atualizado a cada nova execução**, adicionando novos dados e atualizando entradas duplicadas da mesma data/localização.
    * Colunas: `Cargo Pesquisado (Original)`, `Cargo no Glassdoor (Encontrado)`, `Localização`, `Salário Médio Glassdoor`, `Data Coleta`.

2.  **`logs/` (pasta):**
    * Uma subpasta chamada `logs` será criada automaticamente na mesma pasta do executável.
    * Dentro dela, você encontrará arquivos de log no formato: `log_DD-MM-AA_HH-MM.txt` (ex: `log_27-06-2025_14-05.txt`).
    * Cada execução do script gerará um **novo arquivo de log único**.
    * Contém um registro detalhado da execução, incluindo:
        * Horário de início e término do script.
        * Tempo total de execução.
        * Número total de cargos pesquisados.
        * Contagem de salários encontrados com sucesso.
        * Contagem de salários não encontrados ou com erro.
        * Mensagens de aviso e erro durante o processo.

---

## Solução de Problemas Comuns

* **O script não inicia o navegador ou trava logo no início:**
    * **Causa provável:** O Chrome está aberto em segundo plano, ou há um processo `chromedriver.exe` travado.
    * **Solução:** Feche todas as janelas do Chrome e, no Gerenciador de Tarefas (`Ctrl + Shift + Esc`), finalize qualquer `chrome.exe` ou `chromedriver.exe` antes de tentar novamente.
* **"Failed to load Python DLL" / "LoadLibrary: Não foi possível encontrar o módulo especificado":**
    * **Causa provável:** Problemas com a forma como o Python foi instalado na máquina onde o executável foi *criado*, ou um antivírus bloqueando arquivos empacotados.
    * **Solução:** (Na máquina onde o .exe foi criado) Reinstale o Python a partir do site oficial `python.org` (não da Microsoft Store), certificando-se de marcar "Add Python to PATH" durante a instalação. Reinstale as bibliotecas e recrie o executável. Verifique também o antivírus.
* **Login não funciona ou o script trava nos passos de login:**
    * **Causa:** O Glassdoor alterou a estrutura da página de login (IDs, classes, etc.), ou as credenciais no script estão incorretas/expiradas.
    * **Solução:** (Para o desenvolvedor) Será necessário inspecionar a página de login do Glassdoor para encontrar os novos seletores e atualizar o código Python original, para depois recriar o executável. Verifique as credenciais no script Python original.
* **"NoSuchElementException" ou "TimeoutException" durante a pesquisa de cargos:**
    * **Causa:** O Glassdoor alterou a estrutura HTML das páginas de pesquisa/resultado, ou um elemento esperado não carregou a tempo.
    * **Solução:** (Para o desenvolvedor) Inspecione os elementos problemáticos no navegador para encontrar os novos seletores e atualize o script Python original, para depois recriar o executável.
* **Arquivo Excel não salva ou dá erro de permissão:**
    * **Causa:** O arquivo `base_salarios_glassdoor.xlsx` está aberto em algum programa (como o próprio Excel) quando o script tenta escrevê-lo.
    * **Solução:** Certifique-se de que o arquivo Excel esteja **fechado** antes de executar o script.
---

## Contato

Em caso de dúvidas ou problemas, entre em contato:
heros.dinao@pgmais.com