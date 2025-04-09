import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import urllib.parse
from selenium.webdriver.common.keys import Keys
import json
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import smtplib
import os
from email.message import EmailMessage
from models import BaseModel, Audience, Case
import paramiko
from datetime import datetime, timedelta

class Utils:

    """
    Método que permite extraer desde una cadena stringHTML un sun string
    delimitado por initStringDelimiter y endStringDelimiter
    el string resultante no incluye estos dos elementos
    """
    @staticmethod
    # Utilidad para loguear mensajes
    def log(message):
        print(f"[{datetime.now()}] {message}")


    # Función para inicializar WebDriver
    '''
    headless=True: Ejecuta el navegador sin interfaz gráfica.
    headless=False: Ejecuta el navegador en modo normal,
    '''
    @staticmethod
    def initialize_driver(GECKODRIVER_PATH, headless=True):
        options = Options()
        options.headless = headless  # Activa o desactiva el modo sin interfaz
        Utils.log(f"Inicializando driver en modo {'headless' if headless else 'normal'}")
        service = Service(executable_path=GECKODRIVER_PATH)
        return webdriver.Firefox(service=service, options=options)

    # Función para esperar y hacer clic en un elemento
    @staticmethod
    def wait_and_click(driver, by, locator, timeout=60):
        try:
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))
            element.click()
            Utils.log(f"Clic exitoso en el elemento: {locator}")
            return element
        except TimeoutException:
            Utils.log(f"Tiempo de espera excedido para el elemento: {locator}")
            return None

    # Función para esperar un elemento y devolverlo
    @staticmethod
    def wait_for_element(driver, by, locator, timeout=60):
        try:
            element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, locator)))
            Utils.log(f"Elemento localizado: {locator}")
            return element
        except TimeoutException:
            Utils.log(f"No se pudo localizar el elemento: {locator}")
            return None

    # Función para manejar los popups
    @staticmethod
    def close_modal(driver, css_selector='div.modal-footer button[data-dismiss="modal"]'):
        # Buscar el elemento body
        body = driver.find_element(By.TAG_NAME, "body")

        # Enviar la tecla ESCAPE para intentar cerrar el modal
        body.send_keys(Keys.ESCAPE)

        # Crear una acción para hacer clic en el body
        actions = ActionChains(driver)
        actions.move_to_element(body).click().perform()

    # Funcion para leer archivos Json
    @staticmethod
    def loadJson(path):
        try:
            with open(path, encoding="utf-8") as sources_file:
                return json.load(sources_file)
        except Exception as e:
            print(f"Error en la ejecución: {e}")
            return False

    @staticmethod
    def dateMysqlFormat(date):
        try:
            # Convertir la fecha de formato DD/MM/YYYY a un objeto datetime
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            # Convertir el objeto datetime al formato MySQL (YYYY-MM-DD HH:MM:SS)
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Manejo de errores si el formato de fecha no es válido
            return None

    @staticmethod
    def adjustKey(key):
        # Asegurarse de que la clave sea de tipo bytes
        if isinstance(key, str):
            key = key.encode('utf-8')  # Convertir a bytes si es una cadena de texto
        # Asegurarse de que la clave tenga 32 bytes (256 bits)
        if len(key) < 32:
            # Rellenar la clave con ceros (bytes) si es más corta
            key = key.ljust(32, b'\0')  # Usar b'\0' para rellenar con bytes
        elif len(key) > 32:
            # Truncar la clave si es más larga
            key = key[:32]
        return key

    @staticmethod
    def decrypt(encrypted_data, config):
        key = config["secretKey"]
        iv = config["iv"].encode('utf-8')
        # Ajustar la clave a 32 bytes
        key = Utils.adjustKey(key)
        # Decodificar desde base64
        decoded = b64decode(encrypted_data)
        # Crear el objeto Cipher con AES-256-CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        # Descifrar los datos
        decrypted = decryptor.update(decoded) + decryptor.finalize()
        # Eliminar el padding PKCS7
        pad_length = decrypted[-1]
        return decrypted[:-pad_length].decode('utf-8')

    def dateFormatEs(originalDate):
        # Si originalDate es una cadena, intenta convertirla a datetime
        if isinstance(originalDate, str):
            try:
                originalDate = datetime.strptime(originalDate, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return "Formato de fecha inválido"

        # Si originalDate es un objeto datetime, formatea la fecha
        if isinstance(originalDate, datetime):
            return originalDate.strftime("%d/%m/%Y")

        # Si no es ni una cadena ni un datetime, devuelve un mensaje de error
        return "Formato de fecha inválido"

    def dateTimeFormatEs(originalDate):
        # Si originalDate es una cadena, intenta convertirla a datetime
        if isinstance(originalDate, str):
            try:
                originalDate = datetime.strptime(originalDate, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return "Formato de fecha inválido"

        # Si originalDate es un objeto datetime, formatea la fecha
        if isinstance(originalDate, datetime):
            return originalDate.strftime("%d/%m/%Y %H:%M:%S")

        # Si no es ni una cadena ni un datetime, devuelve un mensaje de error
        return "Formato de fecha inválido"

    @staticmethod
    def getDocument(mov, cell, configData):

        # URL base del servidor donde se encuentra el documento
        base_url = configData["URLDocument"]

        formElement = cell.find_element(By.TAG_NAME, "form")
        formAction = formElement.get_attribute("action")

        try:
            inputs = formElement.find_elements(By.NAME, "valorDoc")
            inputElement = inputs[0]
            valorDoc = inputElement.get_attribute("value")
            url = f"{formAction}?valorDoc={urllib.parse.quote(valorDoc)}"
        except:
            inputs = formElement.find_elements(By.NAME, "valorFile")
            inputElement = inputs[0]
            valorFile = inputElement.get_attribute("value")
            url = f"{formAction}?valorFile={urllib.parse.quote(valorFile)}"

        # Definir los headers personalizados
        headers = {
            "Host": "oficinajudicialvirtual.pjud.cl",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cookie": "_ga_DCJFQTPKEZ=GS1.1.1740710815.30.0.1740710815.0.0.0; _ga=GA1.2.1713062412.1736299190; _gid=GA1.2.1818485784.1740669711; PHPSESSID=ab9bb19bf1cf7d95aa3d7d568d8bccc9; TS01262d1d=01b485afe5815c8f410ee846755fdd6289d2d7aaef4927fbaf64048ca0e7d300c92aa2ce312ce590181e578c8f0dd17a4f67aaaeb9bc103602c09d0f51f4efb0ca7f818689"
        }

        # Hacer la solicitud GET con los headers
        response = requests.get(url, headers=headers, allow_redirects=True)

        hash = hashlib.md5(mov.description.encode()).hexdigest()
        documentName = "documento-" + hash + ".pdf"
        documentPath = configData["tempDoc"] + "\\" + documentName

        # Verificar si la respuesta es válida
        if response.status_code == 200:
            # Guardar el archivo PDF en el sistema local
            with open(documentPath, "wb") as file:
                file.write(response.content)
            print(f"✅ Documento descargado con éxito {documentPath}.")
        else:
            print(f"❌ Error al descargar el documento. Código: {response.status_code}")

        if os.path.exists(documentPath):
            return documentPath
        else:
            return None

    @staticmethod
    def cleanWorkingDir(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))


    @staticmethod
    def getDateTimeISO8601(dateTime, time):
        # Convertir la cadena de fecha a un objeto datetime
        dt = datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")

        # Convertir la cadena de tiempo a un objeto time
        t = datetime.strptime(time, "%H:%M").time()

        # Combinar la fecha de `dt` con la hora de `t`
        combined_datetime = datetime.combine(dt.date(), t)

        # Convertir a formato ISO 8601 sin desplazamiento de zona horaria
        iso8601 = combined_datetime.isoformat()

        return iso8601