# api-casos.py
from flask import Flask
from routes.corte_suprema import corte_suprema

app = Flask(__name__)

# Registrar el blueprint con un prefijo común para la API
app.register_blueprint(corte_suprema, url_prefix='/corte_suprema')

if __name__ == '__main__':
    app.run(debug=True)