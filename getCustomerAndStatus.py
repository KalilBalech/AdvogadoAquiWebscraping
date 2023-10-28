from cleanText import clean_text
from selenium.webdriver.common.by import By

def getCustomerAndStatus(driver, lawyerFullName):

    nomeParteEAdvogado = driver.find_elements(By.CSS_SELECTOR, ".nomeParteEAdvogado")
    requerente = nomeParteEAdvogado[0].get_property("innerHTML")
    requerente = clean_text(requerente)
    requerido = nomeParteEAdvogado[1].get_property("innerHTML")
    requerido = clean_text(requerido)

    requerenteLines = requerente.split('\n')
    requeridoLines = requerido.split('\n')

    customerFullName = ''
    requerente = False
    for line in requerenteLines:
        if line == lawyerFullName:
            customerFullName = requerenteLines[0]
            requerente = True
    if customerFullName == '':
        for line in requeridoLines:
            if line == lawyerFullName:
                customerFullName = requeridoLines[0]
    
    return (customerFullName, requerente)