import os
import traceback
from flask import Flask

app = Flask(__name__)

# Ruta raíz para verificar salud
@app.route('/')
def root():
    return '✅ API JJ funcionando', 200

# Carga y registro del blueprint
try:
    from routes.corte_suprema import corte_suprema
    app.register_blueprint(corte_suprema, url_prefix='/corte_suprema')
except Exception as e:
    print("❌ ERROR cargando blueprint:")
    traceback.print_exc()

# Detecta entorno de ejecución
execution_env = os.environ.get("EXECUTION_ENV", "local")
port = int(os.environ.get("PORT", 5001))
debug = (execution_env != "production")

if __name__ == '__main__':
    print(f"🚀 Iniciando API en puerto {port} | modo: {execution_env}")
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)
