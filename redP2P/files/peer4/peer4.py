import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cargar configuración del peer
with open('./peer4_config.json', 'r') as config_file:
    config = json.load(config_file)

# Listar archivos en el directorio configurado
def list_files():
    directory = config['directory']
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Registrar el peer en el servidor de directorio
def register_with_directory():
    peer_data = {
        "peer_id": config['peer_id'],
        "peer_ip": f"http://{config['ip']}:{config['port']}",
        "files": list_files()
    }
    response = requests.post(config['peer_titular'], json=peer_data)
    print("Registro del peer:", response.json())

@app.route('/get_files', methods=['GET'])
def get_files():
    files = list_files()
    return jsonify({"files": files}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.json
    file_name = data['file_name']
    file_content = data['file_content']
    with open(os.path.join(config['directory'], file_name), 'wb') as f:
        f.write(file_content.encode())  # Asume que el contenido del archivo es un string
    return jsonify({"message": "Archivo subido con éxito"}), 200

if __name__ == '__main__':
    register_with_directory()