# Usa una imagen de Python como base
FROM python:3.11.3-slim-buster

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia el resto de los archivos del proyecto
COPY . .

# Cambia el directorio de trabajo a src
WORKDIR /app/src

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]