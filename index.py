from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time # trocar o time.sleep pelo webdriver.wait -> mais inteligente

from pdfminer.high_level import extract_text

import os
from dotenv import load_dotenv
load_dotenv()

CPF = os.environ.get("CPF")
SENHA = os.environ.get("SENHA")

def remove_digits(number_str):
    if len(number_str) != 20:
        raise ValueError("A entrada deve ter exatamente 20 dígitos.")

    # Remover o décimo quarto, décimo quinto e décimo sexto dígitos
    return number_str[:13] + number_str[16:]

def get_last_downloaded_file(download_path):
    # Lista todos os arquivos no diretório
    list_of_files = [os.path.join(download_path, file) for file in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, file))]
    
    # Ordena os arquivos por data de modificação
    sorted_files = sorted(list_of_files, key=os.path.getmtime, reverse=True)
    
    # Retorna o arquivo mais recentemente modificado (ou seja, o último baixado)
    return sorted_files[0] if sorted_files else None

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Arquivo {filepath} excluído com sucesso!")
    else:
        print(f"Arquivo {filepath} não encontrado!")

def create_txt_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def clean_text(text):
    # Divide o texto em linhas
    lines = text.split('\n')
    
    # Mantém apenas as linhas que têm mais de um caractere
    cleaned_lines = [line for line in lines if len(line.strip()) > 1]
    
    # Combina as linhas limpas de volta em um texto
    cleaned_text = '\n'.join(cleaned_lines)
    
    return cleaned_text

def buscaDeProcessoAutomatica(numeroDoProcesso):

    tempoDeCarregamentoDaPagina = 1
    tempoDeEsperaFinal = 5

    options = webdriver.ChromeOptions()

    download_folder = "/home/kalil/AdvogadoAquiDownloads"

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }

    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=options)

    driver.get('https://esaj.tjsp.jus.br/sajcas/login?service=https%3A%2F%2Fesaj.tjsp.jus.br%2Fesaj%2Fj_spring_cas_security_check')

    time.sleep(tempoDeCarregamentoDaPagina)

    cpfInput = driver.find_element(By.ID, "usernameForm")
    cpfInput.send_keys(CPF)

    passwordInput = driver.find_element(By.ID, "passwordForm")
    passwordInput.send_keys(SENHA)

    botao = driver.find_element(By.ID, "pbEntrar")
    botao.click()

    time.sleep(1)

    driver.get('https://esaj.tjsp.jus.br/cpopg/open.do?gateway=true')

    time.sleep(tempoDeCarregamentoDaPagina)

    select_element = driver.find_element(By.ID, 'cbPesquisa')
    select = Select(select_element)

    select.select_by_visible_text('Número do Processo')

    numeroProcInput = driver.find_element(By.ID, "numeroDigitoAnoUnificado")
    numeroProcInput.send_keys(remove_digits(numeroDoProcesso))

    consultar = driver.find_element(By.ID, "botaoConsultarProcessos")
    consultar.click()

    # capturar a janela atual
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    
    visualizarAutos = driver.find_element(By.ID, "linkPasta")
    visualizarAutos.click()

    time.sleep(tempoDeCarregamentoDaPagina)

    # capturar a nova janela
    all_window_handles = driver.window_handles
    new_window_handle = None
    while len(all_window_handles) <= 1:
        all_window_handles = driver.window_handles
    new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
    driver.switch_to.window(new_window_handle)


    # monitorar quanto um novo list item dentro da ul que tá dentro da div#arvore_principal

    # clicar na tag a que tem um htmltext = alguma coisa, pegar o href que tá nessa tag e carregar o pdf, transformar em txt e mandar pro gpt

    conjuntoDeDocumentos = driver.find_element(By.ID, "arvore_principal")
    print("arvore: ", conjuntoDeDocumentos)
    documentosAbertos = conjuntoDeDocumentos.find_elements(By.CSS_SELECTOR,".jstree-node.jstree-open")
    print("numero de documentos abertos: ", len(documentosAbertos))
    documentosFechados = conjuntoDeDocumentos.find_elements(By.CSS_SELECTOR,".jstree-node.jstree-closed")
    print("numero de documentos fechados: ", len(documentosFechados))

    ultimoDocumentoAberto = documentosAbertos[len(documentosAbertos)-3]
    print("ultimoDocumentoAberto: ", ultimoDocumentoAberto)

    time.sleep(tempoDeCarregamentoDaPagina)

    tagAnchorDoUltimoDocumentoAberto = ultimoDocumentoAberto.find_element(By.CSS_SELECTOR,".jstree-anchor")
    print("tagAnchorDoUltimoDocumentoAberto: ", tagAnchorDoUltimoDocumentoAberto)

    # pdf = tagAnchorDoUltimoDocumentoAberto.get_attribute('href')
    # print("pdf: ", pdf)

    tagAnchorDoUltimoDocumentoAberto.click()

    time.sleep(tempoDeCarregamentoDaPagina)

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    print("iframe: ", iframe)

    # Alterne para o contexto do iframe
    driver.switch_to.frame(iframe)

    # Agora você pode interagir com os elementos dentro do iframe
    download_button = driver.find_element(By.CSS_SELECTOR, "button#download")
    print("Button:", download_button)

    driver.execute_script("arguments[0].classList.remove('hiddenMediumView');", download_button)
    download_button.click()

    time.sleep(tempoDeCarregamentoDaPagina)

    # Após o download, obtenha o caminho do último arquivo baixado
    pdf_path = get_last_downloaded_file(download_folder)
    print("pdf_path: ", pdf_path)

    # Verifica se encontrou o arquivo
    if not pdf_path:
        print("Não foi possível encontrar o arquivo baixado.")
        driver.quit()
        return None    # Verifica se encontrou o arquivo

    # Extrai texto do PDF
    text = extract_text(pdf_path)
    cleaned_text = clean_text(text)
    delete_file(pdf_path)


    create_txt_file("pdf_to_txt.txt", cleaned_text)


    time.sleep(tempoDeEsperaFinal)
    # Após interagir com os elementos no iframe, volte ao contexto principal
    driver.switch_to.default_content()
    
    driver.quit()

buscaDeProcessoAutomatica("10313198120238260577")
