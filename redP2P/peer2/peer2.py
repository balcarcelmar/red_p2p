# programa que contiene las funciones que se comunican con el servidor directorio ( peer titular ) por medio de http
import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cargar configuración del peer
with open('./peer2_config.json', 'r') as config_file:
    config = json.load(config_file)

# Listar archivos en el directorio configurado
def list_files():
    directory = config['directory']
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Registrar el peer en el servidor de directorio
def login():
    peer_data = {
        "peer_id": config['peer_id'],
        "peer_ip": f"{config['ip']}:{config['port']}",
        "files": list_files()
    }
    try :
        response = requests.post(config['peer_titular']+'/login', json=peer_data)
        print(response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar el peer en el servidor directorio {config['peer_titular']}: {e}")

#desvincularse de la red p2p
def logout():
    peer_data = {"peer_id": config['peer_id']}
    try:
        response = requests.post(config['peer_titular'] + '/logout', json=peer_data)
        print( response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error al cerrar sesión: {config['peer_titular']}: {e}")

# Actualizar el índice de archivos en el servidor de directorio
def update_index():
    peer_data = {
        "peer_id": config['peer_id'],
        "files": list_files()  # Obtener lista de archivos actualizada
    }
    try:
        response = requests.post(config['peer_titular'] + '/enviarindice', json=peer_data)
        print( response.json()['message'])
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el índice en el servidor directorio {config['peer_titular']}: {e}")

# Función para buscar un archivo en el servidor de directorio
def search_file_in_directory(file_name):
    data = {"file_name": file_name}
    try:
        response = requests.post(config['peer_titular'] + '/buscararchivo', json=data)
        print(response.json()['message'])
        print(json.dumps(response.json()['peers'], indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar el archivo en el servidor directorio {config['peer_titular']}: {e}")
    return response.json()['peers']

#Función para obtener el indice de archivos del sistema
def get_index():
    try:
        response = requests.get(config['peer_titular'] + '/get_peers')
        print("peers disponibles:")
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el indice de archivos del peer titular {config['peer_titular']}: {e}")
