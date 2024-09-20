# Dockerfile for peer1

# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /redp2p

# Copiar los archivos del peer al contenedor
COPY . .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir Flask==2.0.1 werkzeug==2.0.3

# Exponer el puerto que este peer va a utilizar
EXPOSE 3000

# Comando para iniciar el peer
CMD ["python", "directory_server.py"]
