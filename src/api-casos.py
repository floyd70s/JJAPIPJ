#-------------------------------------------------------------------------------
# api-casos.py
# MODO PRODUCCIÓN
#-------------------------------------------------------------------------------
import os
from flask import Flask
from routes.corte_suprema import corte_suprema

app = Flask(__name__)
# Registrar el blueprint con un prefijo común para la API
app.register_blueprint(corte_suprema, url_prefix='/corte_suprema')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    
#-------------------------------------------------------------------------------
# MODO LOCAL
#------------------------------------------------------------------------------
# # api-casos.py
# from flask import Flask
# from routes.corte_suprema import corte_suprema

# app = Flask(__name__)

# # Registrar el blueprint con un prefijo común para la API
# app.register_blueprint(corte_suprema, url_prefix='/corte_suprema')

# if __name__ == '__main__':
#     app.run(debug=True)