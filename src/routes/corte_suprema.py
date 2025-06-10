from flask import Blueprint, jsonify, request, Response
import json
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
import os
from utils.utils import Utils
import time
import os
import services.corte_suprema as corte_suprema_service
import traceback

corte_suprema = Blueprint('corte_suprema', __name__)
load_dotenv()

@corte_suprema.route('/buscar-prueba', methods=['GET'])
def buscar_prueba():
    print("Ingreso a /buscar-prueba")
    
    competencia = request.args.get('competencia')
    corte = request.args.get('corte')
    tribunal = request.args.get('tribunal')
    tipo_busqueda = request.args.get('tipo_busqueda')
    libro = request.args.get('libro')
    rol = request.args.get('rol')
    anio = request.args.get('ano')
    
    # Validamos que todos los parámetros obligatorios estén presentes
    if any(param is None for param in [competencia, corte, tribunal, tipo_busqueda, libro, rol, anio]):
        return jsonify({"error": "Faltan parámetros obligatorios"}), 400
    
    # Ejemplo de datos fijos para la prueba
    data_prueba = {        
        "rol": rol,
        "fecha_ingreso": "02/01/2024",
        "tipo_recurso": "(Civil) Apelación Protección",
        "Caratulado": "LONGART/SERVICIO NACIONAL DE MIGRACIONES DEL INTERIOR Y SEGURIDAD PÚBLICA",
        "estado_causa": "Fallada",
        "corte": "Corte Suprema"
    }    
    return jsonify(data_prueba), 200

@corte_suprema.route('/buscar', methods=['GET'])
def buscar():
    print("📥 Ingreso a /buscar")

    competencia   = request.args.get('competencia')
    corte         = request.args.get('corte')
    tribunal      = request.args.get('tribunal')
    tipo_busqueda = request.args.get('tipo_busqueda')
    libro         = request.args.get('libro')
    rol           = request.args.get('rol')
    ano           = request.args.get('ano')

    # Validación de parámetros
    params = {
        "competencia": competencia,
        "corte": corte,
        "tribunal": tribunal,
        "tipo_busqueda": tipo_busqueda,
        "libro": libro,
        "rol": rol,
        "ano": ano
    }
    missing = [k for k, v in params.items() if v is None]
    if missing:
        print("❌ Parámetros faltantes:", missing)
        return jsonify({"error": f"Faltan parámetros: {missing}"}), 400

    try:
        resultado_busqueda = corte_suprema_service.buscar_causas(**params)

        # Si el resultado contiene un error
        if isinstance(resultado_busqueda, dict) and "error" in resultado_busqueda:
            return jsonify(resultado_busqueda), 500

        print("✅ Resultado:", json.dumps(resultado_busqueda, indent=2, ensure_ascii=False))
        return jsonify(resultado_busqueda), 200

    except Exception as e:
        print("❌ ERROR INTERNO EN /buscar:")
        traceback.print_exc()
        return jsonify({"error": "Error interno", "detalle": str(e)}), 500