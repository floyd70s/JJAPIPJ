FROM selenium/standalone-firefox:latest

# Variables de entorno obligatorias para Render
ENV PORT=10000
ENV MODE=local
ENV EXECUTION_ENV=production

# Instala dependencias del sistema
USER root
RUN apt-get update && apt-get install -y python3-pip

# Crea una carpeta para el código
WORKDIR /app

# Copia tus archivos de proyecto
COPY . /app

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto para Render
EXPOSE 10000

# Comando de arranque
CMD ["python3", "api-casos.py"]
