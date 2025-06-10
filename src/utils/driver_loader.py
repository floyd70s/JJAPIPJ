import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "").lower()
GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH")

def get_driver(headless=True, intentos=5, espera=5, options=None):
    if options is None:
        options = Options()
        options.headless = headless

    if MODE == "local":
        if not GECKODRIVER_PATH:
            raise RuntimeError("❌ GECKODRIVER_PATH no está definido para modo local.")
        print("🟢 MODO LOCAL con GECKODRIVER_PATH =", GECKODRIVER_PATH)
        service = Service(executable_path=GECKODRIVER_PATH)
        return webdriver.Firefox(service=service, options=options)

    if MODE == "docker":
        print("🐳 MODO DOCKER (remoto). Conectando a Selenium...")
        return _try_remote_driver(options, intentos, espera)

    # Modo mixto
    print("🔄 MODO MIXTO: intenta primero local")
    if GECKODRIVER_PATH:
        try:
            service = Service(executable_path=GECKODRIVER_PATH)
            return webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print("⚠️ WebDriver local falló:", e)

    return _try_remote_driver(options, intentos, espera)

def _try_remote_driver(options, intentos, espera):
    for intento in range(1, intentos + 1):
        try:
            print(f"🌐 Intento {intento}/{intentos} de conexión remota a Selenium...")
            driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options=options
            )
            print("✅ WebDriver remoto iniciado con éxito.")
            return driver
        except Exception as e:
            print(f"❌ Fallo en intento {intento}: {e}")
            traceback.print_exc()
            time.sleep(espera)

    raise RuntimeError("❌ No se pudo iniciar WebDriver ni en modo local ni remoto.")
