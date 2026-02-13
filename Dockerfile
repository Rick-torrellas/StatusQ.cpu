# Usamos una imagen base oficial de Python (versión slim para menor tamaño)
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el código fuente (necesario para leer pyproject.toml e instalar)
COPY . .

# Instalamos el proyecto y sus dependencias definidas en pyproject.toml
RUN pip install --no-cache-dir .

# Aseguramos que el directorio de logs exista
RUN mkdir -p logs

# Definimos variables de entorno para que Python no bufferice la salida (útil para logs en Docker)
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]