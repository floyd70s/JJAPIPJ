from flask import jsonify
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv
from utils.utils import Utils
from utils.driver_loader import get_driver
import os

load_dotenv()

def buscar_causas(competencia, corte, tribunal, tipo_busqueda, libro, rol, ano):
    driver = None
    try:
        # Configuración de navegador
        options = Options()
        options.headless = True
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        )

        # Inicia WebDriver
        driver = get_driver(headless=True, options=options)

        url_oficina = os.getenv('URLOficinaVirtual', '')
        url_busqueda = url_oficina.replace('indexN.php', 'home/index.php')
        print("🌐 Abriendo página:", url_busqueda)
        driver.get(url_busqueda)

        Utils.wait_and_click(driver, By.CSS_SELECTOR, ".col-sm-4:nth-child(3) .dropbtn")

        if competencia and competencia.strip():
            comp_dd = Utils.wait_for_element(driver, By.ID, "competencia")
            comp_dd.find_element(By.XPATH, f"//option[. = '{competencia}']").click()

        if competencia == "Corte Suprema" and tipo_busqueda and tipo_busqueda.strip() and tipo_busqueda != '""':
            dd = Utils.wait_for_element(driver, By.ID, "conTipoBus")
            dd.find_element(By.XPATH, f"//option[. = '{tipo_busqueda}']").click()
        elif competencia == "Corte Apelaciones" and tipo_busqueda and tipo_busqueda.strip() and tipo_busqueda != '""':
            dd = Utils.wait_for_element(driver, By.ID, "conTipoBusApe")
            dd.find_element(By.XPATH, f"//option[. = '{tipo_busqueda}']").click()

        if corte and corte.strip() and corte != '""':
            dd = Utils.wait_for_element(driver, By.ID, "conCorte")
            dd.find_element(By.XPATH, f"//option[. = '{corte}']").click()

        if tribunal and tribunal.strip() and tribunal != '""':
            dd = Utils.wait_for_element(driver, By.ID, "conTribunal")
            dd.find_element(By.XPATH, f"//option[. = '{tribunal}']").click()

        if competencia == "Corte Suprema" and libro and libro.strip() and libro != '""':
            dd = Utils.wait_for_element(driver, By.ID, "conTipoCausa")
            dd.find_element(By.XPATH, f"//option[. = '{libro}']").click()

        if rol:
            Utils.wait_for_element(driver, By.ID, "conRolCausa").send_keys(rol)
        if ano:
            Utils.wait_for_element(driver, By.ID, "conEraCausa").send_keys(ano)

        Utils.wait_and_click(driver, By.ID, "btnConConsulta")

        tabla = Utils.wait_for_element(driver, By.ID, "dtaTableDetalle")
        filas = tabla.find_elements(By.CSS_SELECTOR, "tbody tr")
        resultados = []
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            if len(celdas) >= 7:
                resultados.append(Asignar_tabla_Respuesta(competencia, celdas))

        return resultados

    except Exception as e:
        print("❌ Error en buscar_causas:", e)
        return {"error": str(e)}

    finally:
        if driver:
            driver.quit()


def Asignar_tabla_Respuesta(competencia, celdas):
    if competencia in ("Corte Suprema", "Corte Apelaciones"):
        return {
            "rol":           celdas[1].text.strip(),
            "tipo_recurso":  celdas[2].text.strip(),
            "caratulado":    celdas[3].text.strip(),
            "fecha_ingreso": celdas[4].text.strip(),
            "estado_causa":  celdas[5].text.strip(),
            "corte":         celdas[6].text.strip(),
        }
    else:
        return {
            "rol":             celdas[2].text.strip(),
            "corte":           celdas[3].text.strip(),
            "caratulado":      celdas[4].text.strip(),
            "fecha_ingreso":   celdas[5].text.strip(),
            "estado_causa":    celdas[6].text.strip(),
            "fecha_ubicacion": celdas[7].text.strip(),
            "ubicacion":       celdas[8].text.strip(),
        }
