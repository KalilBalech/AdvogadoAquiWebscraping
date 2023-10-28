from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import time
import os

from removeDigits import remove_digits

def inquiryCaseByNumber(numeroDoProcesso):

    CPF = os.environ.get("CPF")
    SENHA = os.environ.get("SENHA")
    tempoDeCarregamentoDaPagina = int(os.environ.get("LOADING_PAGE_TIME"))
    
    options = webdriver.ChromeOptions()

    download_folder = os.environ.get("DOWNLOAD_FOLDER")

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

    return driver