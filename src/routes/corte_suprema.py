from flask import Blueprint, jsonify, request
import json
import services.corte_suprema as corte_suprema_service

corte_suprema = Blueprint('corte_suprema', __name__)

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
    print("Ingreso a /buscar")
    
    competencia = request.args.get('competencia')
    corte = request.args.get('corte')
    tribunal = request.args.get('tribunal')
    tipo_busqueda = request.args.get('tipo_busqueda')
    libro = request.args.get('libro')
    rol = request.args.get('rol')
    ano = request.args.get('ano')
    
    # Se arma un dict con todos los parámetros
    params = {
        "competencia": competencia,
        "corte": corte,
        "tribunal": tribunal,
        "tipo_busqueda": tipo_busqueda,
        "libro": libro,
        "rol": rol,
        "ano": ano
    }
    
    # Filtra los parámetros que estén ausentes (None)
    missing = [key for key, value in params.items() if value is None]
    if missing:
        print("Parámetros faltantes:", missing)
        return jsonify({"error": f"Faltan parámetros obligatorios: {missing}"}), 400
    
    resultado_busqueda = corte_suprema_service.buscar_causas(
        competencia=competencia,
        corte=corte,
        tribunal=tribunal,
        tipo_busqueda=tipo_busqueda,
        libro=libro,
        rol=rol,
        ano=ano
    )
    
    # Imprime el resultado en formato JSON en la consola
    print("Resultado:", json.dumps(resultado_busqueda, indent=2, ensure_ascii=False))
    
    return jsonify(resultado_busqueda), 200
