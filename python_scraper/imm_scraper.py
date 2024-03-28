from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import datetime
import os
import concurrent.futures as cf
import time

# Opzioni del browser Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--incognito")






def calcola_attesa(driver, regione, lista):
    try:
        wait = WebDriverWait(driver, timeout=20)
        # Aspetta fino a quando l'elemento con l'ID 'myElement' non diventa visibile
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/div[1]/div/div[3]/div/h1')))
    except:
        # Se l'elemento non diventa visibile entro il tempo massimo di attesa, stampa un messaggio di errore
        print(f"{regione} Timeout! {datetime.datetime.now()}")
        print(f'URL: {driver.current_url}')
        stampa_file(lista, regione)
        driver.quit()
        get_dati_regione(regione)
        return 'stop'
        
    return

def calcola_attesa2(driver):
    try:
        wait = WebDriverWait(driver, timeout=20)
        # Aspetta fino a quando l'elemento con l'ID 'myElement' non diventa visibile
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section[2]/div[1]/div/div[3]/div/h1')))
        
    except:
        return 'NaN'    
    return


def get_att_CSS(driver, argom):
    try:
        return driver.find_element(By.CSS_SELECTOR, f"[aria-label='{argom}']").text
    except:
        return 'NaN'
    
def get_att_xpath(driver, argom):
    try:
        return driver.find_element(By.XPATH, argom).text
    except:
        return 'NaN'

# Trova tutti gli elementi sulla pagina
    
def get_attribute(driver):
    title = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/div[3]/div/h1')
    comune = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/div[3]/div/a/span[1]')
    localita = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/div[3]/div/a/span[2]')
    contratto = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/dl[1]/dd[2]')
    tipologia = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/dl[1]/dd[3]')
    prezzo = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/ul[2]/li[1]')
    locali = get_att_CSS(driver, 'locali')
    superficie = get_att_CSS(driver, 'superficie')
    bagni = get_att_CSS(driver, 'bagni')
    piano = get_att_CSS(driver, 'piano')
    ascensore = get_att_CSS(driver, 'ascensore')
    riscaldamento = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/dl[3]/dd[3]')
    classe_energetica = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/dl[3]/dd[5]')
    prezzo2 = get_att_xpath(driver, '/html/body/div[2]/section[2]/div[1]/div/dl[2]/dd[1]')
    record_annuncio = [title, comune, localita, contratto, tipologia, prezzo, locali, superficie, bagni, piano, ascensore, riscaldamento, classe_energetica, prezzo2]
    
    return record_annuncio
  
def stampa_file(lista, regione, x, n_annunci, passo):

    lista = [[str(cell).replace('\n', '').replace(',', '-') for cell in row] for row in lista]
    
    # Percorso della cartella di destinazione
    folder_path = f"C:/Users/berna/OneDrive/Desktop/Programmazione/Python/EPICODE/Capstone/dati_raccolti/03_2024/{regione}"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Nome del file CSV
    csv_file = f'dati_{regione}_{x+1}_{x+passo}_{n_annunci}_annunci.csv'

    # Percorso completo del nuovo file CSV
    csv_file_path = os.path.join(folder_path, csv_file)

    with open(csv_file_path, mode='w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file)
        writer.writerows(lista)
    return

def get_numero_annunci(driver):
    try:
        risultato_ricerca = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[1]/div[1]/div[1]/div[1]')
        risultato_ricerca_lista = risultato_ricerca.text.split()
        numero_annunci_text = risultato_ricerca_lista[0].split('.')
    except:
        return 0
    try:
        numero_annunci = int(''.join(numero_annunci_text))
    except:
        return 0
    return numero_annunci

def get_numero_annunci_tot(driver, regione):
    prezzo_massimo_url = f'https://www.immobiliare.it/vendita-case/{regione}/?criterio=prezzo&ordine=desc'
    driver.get(prezzo_massimo_url)
    risultato_ricerca = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[1]/div[1]/div[1]/div[1]')
    risultato_ricerca_lista = risultato_ricerca.text.split()
    numero_annunci_text = risultato_ricerca_lista[0].split('.')
    try:
        numero_annunci = int(''.join(numero_annunci_text))
    except:
        return 0
    return numero_annunci

elenco_regioni = ['lombardia',
                  'emilia-romagna',
                  'lazio', 'abruzzo', 'marche',
                  'piemonte', 'liguria', 'veneto',
                  'sicilia', 'puglia',
                  'umbria', 'toscana', 'campania']

regioni_n_annunci = {'lombardia': 0,
                  'emilia-romagna': 0,
                  'lazio': 0, 'abruzzo': 0, 'marche': 0,
                  'piemonte': 0, 'liguria': 0, 'veneto': 0,
                  'sicilia': 0, 'puglia': 0,
                  'umbria': 0, 'toscana': 0, 'campania': 0}

def open_tab(driver):
    n_click = 0
    for x in range(1,30):
        try:
            annunci = driver.find_element(By.XPATH, f'/html/body/div[2]/main/section[1]/div[1]/ul[2]/li[{x}]/div/div[2]/a')
            annunci.click()
            n_click += 1
        except:
            continue
    return n_click

def get_n_pagine():
    return

def close_tab(driver, n_click, lista):
    for x in range(1, n_click + 1):
        newURl = driver.window_handles[1]
        driver.switch_to.window(newURl) 
        if calcola_attesa2(driver) == 'NaN':
            driver.close()
        else:
            lista.append(get_attribute(driver))
            driver.close()
            
    return 

def nuova_pagina(driver, url):
    newURl = driver.window_handles[0]
    driver.switch_to.window(newURl)
    driver.get(url)

def get_prezzo_massimo(driver, regione):
    prezzo_massimo_url = f'https://www.immobiliare.it/vendita-case/{regione}/?criterio=prezzo&ordine=desc'
    driver.get(prezzo_massimo_url)
    prezzo_massimo_obj = driver.find_element(By.XPATH, '/html/body/div[2]/main/section[1]/div[1]/ul[2]/li[1]/div/div[2]/div[2]/span')
    prezzo_massimo_text = prezzo_massimo_obj.text.split()
    prezzo_massimo_list = prezzo_massimo_text[1].split('.')
    prezzo_massimo = int(''.join(prezzo_massimo_list))
    return prezzo_massimo

def get_dati_regione(regione, y, n_fatt, passo = 1000):

    contatore = 0
    inizio = datetime.datetime.now()
    n_annunci_fatti = n_fatt
    obiettivo_perc = 10

    driver = webdriver.Chrome(options=chrome_options)    #options=chrome_options

    regioni_n_annunci[regione] = (get_numero_annunci_tot(driver, regione))


    prezzo_massimo = get_prezzo_massimo(driver, regione)

    print(f'Inizio {regione}: ore {inizio}')

    for x in range(y, prezzo_massimo + passo + 1, passo):
        contatore += 1

        annunci_regione = [['title', 'comune', 'localita',
                        'contratto', 'tipologia', 'prezzo', 'locali',
                        'superficie', 'bagni', 'piano',
                            'ascensore', 'riscaldamento', 'classe_energetica', 'prezzo_di_sicurezza']]

        url = f'https://www.immobiliare.it/vendita-case/{regione}/?criterio=rilevanza&prezzoMinimo={x+1}&prezzoMassimo={x+passo}'
        driver.get(url)

        n_annunci = get_numero_annunci(driver)
        
        if n_annunci == 0:
            continue
        
        for w in range(0, n_annunci//25 + 1):
            n_click = open_tab(driver)  

            close_tab(driver, n_click, annunci_regione)

            nuova_pagina(driver, f'https://www.immobiliare.it/vendita-case/{regione}/?criterio=rilevanza&prezzoMinimo={x+1}&prezzoMassimo={x+passo}&pag={w+2}')

        
        n_annunci_fatti += n_annunci
        percentuale = n_annunci_fatti / regioni_n_annunci[regione] * 100
        if percentuale >= obiettivo_perc:
            tempo_parziale = datetime.datetime.now()
            print(f'{regione} al {percentuale}%')
            print(f'{regione}: annunci fatti: {n_annunci_fatti} su {regioni_n_annunci[regione]} in {tempo_parziale - inizio}')
            obiettivo_perc += 10

        if contatore % 20 == 0:
            driver.quit()
            driver = webdriver.Chrome(options=chrome_options)
        stampa_file(annunci_regione, regione, x, n_annunci, passo)
                   

    fine = datetime.datetime.now()

    print(f'{regione}: {inizio}', f'{regione}: {fine}', sep='\n')
    driver.quit()
    



get_dati_regione('molise', 0, 0)





'''
max_threads = 10
with cf.ThreadPoolExecutor(max_workers=max_threads) as executor:
    executor.map(get_dati_regione, elenco_regioni)

'''
