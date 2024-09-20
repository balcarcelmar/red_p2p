from flask import Flask, request, jsonify
import json

app = Flask(__name__)

peers = {}  # Diccionario para almacenar los peers y sus archivos

@app.route('/login', methods=['POST'])
# Obtener los datos de la solicitud (enviados como JSON por el peer)
def login():

    data = request.json 
    peer_id = data['peer_id']   # Identificador único del peer
    peer_ip = data['peer_ip']   # Dirección IP del peer
    files = data['files']       # Lista de archivos que el peer tiene

# Registrar el peer en el diccionario 'peers'
    peers[peer_id] = {
        'ip': peer_ip,
         'files': files
        }
#respuesta a mostrar
    response_data = {
        "message": f"{peer_id} registrado correctamente en el servidor directorio"
    }
#imprimir en consola
    print(f"{peer_id} registrado correctamente")
    print(peers)

# Devolver una respuesta de éxito
    return jsonify(response_data), 200

@app.route('/logout', methods=['POST'])
def logout():
    data = request.json 
    peer_id = data['peer_id'] 
    if peer_id in peers:
        peers.pop(peer_id)
        print(peers)
        response_data = {
            "message": f"{peer_id} eliminado con exito",
        }
        print(peers)
        return jsonify(response_data),200
    else :
        response_data = {
            "message": f"Error: {peer_id} no está registrado"
        }
        return jsonify(response_data), 400



#Actualización del índice
@app.route('/enviarindice', methods=['POST'])

def update_index():
    data = request.json
    peer_id = data['peer_id']
    files = data['files']

    # Verificar si el peer está registrado
    if peer_id in peers:
        # Actualizar el índice de archivos del peer
        peers[peer_id]['files'] = files
        response_data = {
            "message": f"Índice de {peer_id} actualizado con éxito",
        }
        # Imprimir en consola para verificar
        print(f"Actualización del índice del peer {peer_id}:")
        print(peers[peer_id])
    else:
        # Si el peer no está registrado, devolver un error
        response_data = {
            "message": f"Error: {peer_id} no está registrado"
        }
        return jsonify(response_data), 400
   

    return jsonify(response_data), 200


@app.route('/get_peers', methods=['GET'])
def get_peers():
    return jsonify(peers), 200

# Ruta para buscar un archivo en la red de peers
@app.route('/buscararchivo', methods=['POST'])
def search_file():
    data = request.json
    file_name = data.get('file_name')

    # Lista para almacenar los peers que tienen el archivo
    peers_with_file = []

    # Buscar en todos los peers si tienen el archivo
    for peer_id, peer_info in peers.items():
        if file_name in peer_info['files']:
            peers_with_file.append({
                'peer_id': peer_id,
                'peer_ip': peer_info['ip']
            })

    if len(peers_with_file):
        return jsonify({"message": "Archivo encontrado en los siguientes peers:", "peers": peers_with_file}), 200
    else:
        return jsonify({"message": "Archivo no encontrado","peers":peers_with_file}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
