import time # trocar o time.sleep pelo webdriver.wait -> mais inteligente
import os

from aux.createTxtFile import create_txt_file
from main.gptPromptInstructions import gptPromptInstructions

from main.inquiryCaseByNumber import inquiryCaseByNumber
from main.getCustomerAndStatus import getCustomerAndStatus
from main.getLastDocument import getLastDocument

from aux.sendEmail import enviar_email

from dotenv import load_dotenv
load_dotenv()

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

processNumber = "10131614620218260577"

def buscaDeProcessoAutomatica(numeroDoProcesso):

    tempoDeCarregamentoDaPagina = int(os.environ.get("LOADING_PAGE_TIME"))
    tempoDeEsperaFinal = int(os.environ.get("FINAL_WAITING_TIME"))

    lawyerFullName = 'Ana Luiza Picolli Siqueira'
    lawyerCallingName = 'Ana Luiza'
    officeName = 'PicollieVaz'

    # consulta de processo pelo número, com o advogado logado
    driver = inquiryCaseByNumber(numeroDoProcesso)

    # descobrir o nome do cliente, e se ele é requerente ou requerido
    (customerFullName, requerente) = getCustomerAndStatus(driver, lawyerFullName)
    customerFirstName = customerFullName.split(' ')[0]


    # pegar o texto do ultimo auto do processo

    (driver, text) = getLastDocument(driver)
    gptInstructions = gptPromptInstructions(lawyerCallingName, officeName, customerFirstName, requerente)

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": gptInstructions},
        {"role": "user", "content": text}
    ]
    )

    message = completion.choices[0].message.content

    print(completion)
    create_txt_file("emailMessage.txt", message)

    time.sleep(tempoDeCarregamentoDaPagina)

    enviar_email(message)

    time.sleep(tempoDeCarregamentoDaPagina)
        
    driver.quit()

buscaDeProcessoAutomatica(processNumber)
