FROM selenium/standalone-firefox:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

# Configurar PYTHONPATH para incluir el directorio /app
ENV PYTHONPATH="/app"

# copia solo el contenido de src y los archivos de configuración
COPY src/ /app
COPY .env requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python", "api-casos.py"]