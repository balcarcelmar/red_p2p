import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cargar configuración del peer
with open('./peer3_config.json', 'r') as config_file:
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
    response = requests.post(config['peer_titular'] + '/enviarindice', json=peer_data)
    print("Registro del peer:", response.json())


# Actualizar el índice de archivos en el servidor de directorio
def update_index():
    peer_data = {
        "peer_id": config['peer_id'],
        "files": list_files()  # Obtener lista de archivos actualizada
    }
    try:
        response = requests.post(config['peer_titular'] + '/enviarindice', json=peer_data)
        print("Actualización del índice del peer:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar el índice en el peer titular {config['peer_titular']}: {e}")


@app.route('/get_files', methods=['GET'])
def get_files():
    files = list_files()
    return jsonify({"files": files}), 200

# Subir un archivo y actualizar el índice en el servidor de directorio
@app.route('/upload', methods=['POST'])
def upload_file():
    data = request.json
    file_name = data['file_name']
    file_content = data['file_content']
    
    # Guardar el archivo en el directorio del peer
    with open(os.path.join(config['directory'], file_name), 'wb') as f:
        f.write(file_content.encode())  # Asume que el contenido del archivo es un string
    
    # Actualizar el índice de archivos en el servidor de directorio o con otro peer
    update_index()
    
    return jsonify({"message": "Archivo subido y índice actualizado con éxito"}), 200

if __name__ == '__main__':
    register_with_directory()