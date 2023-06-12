## Run selenium and chrome driver to scrape data from cloudbytes.dev
import sys, os, shutil, glob, tempfile, time, requests
import json
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select




def handler(event=None, context=None):

    r1 = requests.post('https://api.nobordist.com/authenticate?email=ddpbot@nobordist.com&password=Acar4j3do887!', headers={'Content': 'application/json'})
    token = r1.json().get("auth_token")
    auth = 'Bearer ' + token
    r2 = requests.get('https://api.nobordist.com/v1/volumes-mi-statuses', headers={'Content': 'application/json', 'Authorization': auth})
    try:
        numbers = r2.json().get("data").get("numbers")
    except:
        print(r2.status_code)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("window-size=2560x1440")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
  

    browser = webdriver.Chrome("/opt/chromedriver", options=chrome_options)
    browser.get("https://apps.correios.com.br/portalimportador/pages/pesquisarRemessaImportador/pesquisarRemessaImportador.jsf")
    time.sleep(1)
    print('Loggin in')
    username = browser.find_element(By.ID, "username")
    password = browser.find_element(By.ID, "password")
    username.send_keys("41723868000105")
    password.send_keys("nobordist@123")
    time.sleep(1)
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div[1]/section/div/div/form/div[2]/button"))).click()
    time.sleep(1)
    print('starting list')
    #numbers = ['RV226244487UZ', 'oijjzejiojiz', 'NB030770400BR']
    response = []
    for number in numbers:
        try:
            print('entered the loop')
            print(number[0])
            obj = browser.find_element(By.ID, "form-pesquisarRemessas:codigoEncomenda")
            obj.clear()
            obj.send_keys(number[0])
            time.sleep(0.5)
            WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.ID, "form-pesquisarRemessas:btnPesquisar"))).click()
            time.sleep(1)
            status = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[2]/form/div[4]/table/tbody/tr[2]/td[5]"))).text
            print(status)
            response.append({'id': number[1], 'status': status})
        except:
            print('we arrived in except')
            browser.get("https://apps.correios.com.br/portalimportador/pages/pesquisarRemessaImportador/pesquisarRemessaImportador.jsf")
            time.sleep(1)
    print('end loop')
    r4 = requests.put('https://api.nobordist.com/v1/alert_logs/mi-statuses', 
    headers={'Content': 'application/json', 'Authorization': auth},
    data = {'elements': json.dumps(response)}
    )
    print(r4.status_code)
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
    browser.quit()