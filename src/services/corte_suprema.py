from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

from dotenv import load_dotenv
from utils.utils import Utils
import time
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()
app = Flask(__name__)

def buscar_causas(competencia, corte, tribunal, tipo_busqueda, libro, rol, ano):
    driver = None
    try:
        
        geckodriver_path = os.getenv('GECKODRIVER_PATH_PROD')
        url_oficina = os.getenv('URLOficinaVirtual')
        url_busqueda = url_oficina.replace('indexN.php', 'home/index.php')
         
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        print(f"Iniciando Firefox con GeckoDriver en: {geckodriver_path}")
        service = Service(executable_path=geckodriver_path)        
        driver = webdriver.Firefox(service=service, options=options)
        print("Se inicializó el driver de Firefox")
        
        driver.get(url_busqueda)        
        print("Se abrió la URL", url_busqueda)
        
        Utils.wait_and_click(driver, By.CSS_SELECTOR, ".col-sm-4:nth-child(3) .dropbtn")
             
                         
        # Seleccionar la opción correspondiente en el dropdown de competencias
        dropdown = Utils.wait_for_element(driver, By.ID, "competencia")       
        dropdown.find_element(By.XPATH, f"//option[. = '{competencia}']").click()
        print("1.- competencia encontrada:", competencia)
        
        
        if tipo_busqueda and competencia == "Corte Suprema":
            dropdown = Utils.wait_for_element(driver, By.ID, "conTipoBus")
            dropdown.find_element(By.XPATH, f"//option[. = '{tipo_busqueda}']").click()   
            print("2.-tipo de busqueda encontrada para corte suprema:", tipo_busqueda)
            # time.sleep(5)
            
        if tipo_busqueda and competencia == "Corte Apelaciones":
            dropdown = Utils.wait_for_element(driver, By.ID, "conTipoBusApe")
            dropdown.find_element(By.XPATH, f"//option[. = '{tipo_busqueda}']").click()   
            print("2.-tipo de busqueda encontrada para corte apelaciones:", tipo_busqueda)
            # time.sleep(5)
        
        if corte:
            dropdown = Utils.wait_for_element(driver, By.ID, "conCorte")
            dropdown.find_element(By.XPATH, f"//option[. = '{corte}']").click()
            print("3.-corte encontrada:", corte)
            # time.sleep(5)

        if tribunal:
            dropdown = Utils.wait_for_element(driver,By.ID, "conTribunal")
            dropdown.find_element(By.XPATH, f"//option[. = '{tribunal}']").click()
            print("4.-tribunal encontrado:", tribunal)
            # time.sleep(5)
                
        if libro and competencia == "Corte Suprema" and tipo_busqueda in("Recurso Corte Suprema","Recurso Corte Apelaciones"): 
            dropdown = Utils.wait_for_element(driver, By.ID, "conTipoCausa")
            dropdown.find_element(By.XPATH, f"//option[. = '{libro}']").click()
            print("5.-libro encontrado:", libro)
            # time.sleep(5)
                        
        if competencia == "Corte Suprema" or competencia == "Corte Apelaciones":
            print ("ejecucion de la busqueda")        
            Utils.wait_and_click(driver, By.ID, "conRolCausa")
            Utils.wait_and_click(driver, By.ID, "conRolCausa").send_keys(rol)
            print("6.-rol para Corte Suprema o Corte apelaciones encontrado:", rol)
            # time.sleep(5)
            
        elif competencia == "Civil":
            Utils.wait_and_click(driver, By.ID, "conTipoCausa")
            Utils.wait_and_click(driver, By.ID, "conTipoCausa").send_keys(rol)         
            print("6.-rol para Civil encontrado:", rol)
            # time.sleep(5)
            
        Utils.wait_and_click(driver, By.ID, "conEraCausa").click()
        Utils.wait_and_click(driver, By.ID, "conEraCausa").send_keys(ano)
        print ("7.-ano encontrado:", ano)
                     
        # time.sleep(10)
        Utils.wait_and_click(driver, By.ID, "btnConConsulta").click()
        print ("8.-se hace click en el boton buscar")

        # Extracción de datos de la tabla, etc.
        tabla = Utils.wait_for_element(driver, By.ID, "dtaTableDetalle")
        
        filas = tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
        resultados = []
        datos= []
        
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")            
            if len(celdas) >= 7:
                datos= Asignar_tabla_Respuesta(competencia,celdas)
                resultados.append(datos)
               
        return resultados
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if driver:
            driver.quit()

def Asignar_tabla_Respuesta(competencia, celdas):
    #print("-------------------------------------")
    #print("Asignar_tabla_Respuesta")    
    #print("Competencia:", competencia)
    #print("Número de celdas encontradas:", len(celdas))
    #print("-------------------------------------")
    if competencia == "Corte Suprema" or competencia == "Corte Apelaciones":
        datos = {
            "rol": celdas[1].text.strip(),
            "tipo_recurso": celdas[2].text.strip(),
            "caratulado": celdas[3].text.strip(),
            "fecha_ingreso": celdas[4].text.strip(),
            "estado_causa": celdas[5].text.strip(),
            "corte": celdas[6].text.strip()
        }
        #print("Datos extraídos:", datos["caratulado"])
        return datos 

    elif competencia == "Civil":
        datos = {
            "rol": celdas[2].text.strip(),
            "corte": celdas[3].text.strip(),
            "caratulado": celdas[4].text.strip(),
            "Fecha Ingreso": celdas[5].text.strip(),
            "Estado Causa": celdas[6].text.strip(),
            "Fecha Ubicación": celdas[7].text.strip(),
            "Ubicación": celdas[8].text.strip()
        }
        return datos