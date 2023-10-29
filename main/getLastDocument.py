from selenium.webdriver.common.by import By

from aux.getLastDownloadFile import get_last_downloaded_file
from aux.cleanText import clean_text
from aux.createTxtFile import create_txt_file
from aux.deleteFile import delete_file
from pdfminer.high_level import extract_text




import os
import time

def getLastDocument(driver):

    tempoDeCarregamentoDaPagina = int(os.environ.get('LOADING_PAGE_TIME'))
    tempoDeEsperaFinal = int(os.environ.get("FINAL_WAITING_TIME"))

    download_folder = os.environ.get('DOWNLOAD_FOLDER')


    # capturar a janela atual para depois mudar para a nova janela
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    
    # clicar em visualizar autos, o que abre uma nova janela
    visualizarAutos = driver.find_element(By.ID, "linkPasta")
    visualizarAutos.click()

    time.sleep(tempoDeCarregamentoDaPagina)

    # entrar na nova janela aberta
    # capturar a nova janela
    all_window_handles = driver.window_handles
    new_window_handle = None
    while len(all_window_handles) <= 1:
        all_window_handles = driver.window_handles
    new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
    driver.switch_to.window(new_window_handle)


    # monitorar quanto um novo list item dentro da ul que tá dentro da div#arvore_principal

    # encontrar todos os autos
    conjuntoDeDocumentos = driver.find_element(By.ID, "arvore_principal")
    documentosAbertos = conjuntoDeDocumentos.find_elements(By.CSS_SELECTOR,".jstree-node.jstree-open")
    #documentosFechados = conjuntoDeDocumentos.find_elements(By.CSS_SELECTOR,".jstree-node.jstree-closed")


    documentsTitles = []
    for document in documentosAbertos:
        aTag = document.find_element(By.CSS_SELECTOR, ".jstree-anchor")
        aInnerHTML = aTag.get_attribute('innerHTML')
        for i in range(len(aInnerHTML)-1, -1, -1):  # Começa do último caractere e vai até o primeiro
            if aInnerHTML[i] == '>':
                documentsTitles.append(aInnerHTML[i+1:])
                break

    print('documentsTitles: ', documentsTitles)
    shift = 0
    for i in range(len(documentsTitles)-1, -1, -1):
        if(documentsTitles[i] == 'Certidão' or documentsTitles[i] == 'Certidão de Publicação' or documentsTitles[i] == 'Documentos Diversos'):
            shift += 1
        else:
            break
    
    print("shift: ", shift)

    time.sleep(tempoDeCarregamentoDaPagina)
    
    # selecionar o auto que eu quero
    documentoAlvo = documentosAbertos[len(documentosAbertos)-1 - shift]

    # encontrar e clicar no link do auto que eu quero
    tagAnchorDocumentoAlvo = documentoAlvo.find_element(By.CSS_SELECTOR,".jstree-anchor")
    tagAnchorDocumentoAlvo.click()

    time.sleep(tempoDeCarregamentoDaPagina)

    # encontrar o iframe, onde está o botão de baixar pdf
    iframe = driver.find_element(By.TAG_NAME, "iframe")

    # Alterne para o contexto do iframe
    driver.switch_to.frame(iframe)

    # Agora você pode interagir com os elementos dentro do iframe
    #encontrar botão de baixar pdf
    download_button = driver.find_element(By.CSS_SELECTOR, "button#download")

    # deixar o botão de baixar pdf clicável
    driver.execute_script("arguments[0].classList.remove('hiddenMediumView');", download_button)

    #clicar no botão de baixar pdf
    download_button.click()

    time.sleep(tempoDeEsperaFinal)

    # Após o download, obtenha o caminho do último arquivo baixado
    pdf_path = get_last_downloaded_file(download_folder)

    # Verifica se encontrou o arquivo
    if not pdf_path:
        print("Não foi possível encontrar o arquivo baixado.")
        driver.quit()
        return None    # Verifica se encontrou o arquivo

    # Extrai texto do PDF
    text = extract_text(pdf_path)
    cleaned_text = clean_text(text)
    create_txt_file("pdf_to_txt.txt", cleaned_text)
    delete_file(pdf_path)
    # Após interagir com os elementos no iframe, volte ao contexto principal
    driver.switch_to.default_content()

    return (driver, cleaned_text)