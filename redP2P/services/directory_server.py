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
        "peers": peers
    }
#imprimir en consola
    print("Respuesta que se enviará al cliente:")
    print(json.dumps(response_data, indent=4)) 

# Devolver una respuesta de éxito
    return jsonify(response_data), 200


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
            "peers": peers
        }
    else:
        # Si el peer no está registrado, devolver un error
        response_data = {
            "message": f"Error: {peer_id} no está registrado"
        }
        return jsonify(response_data), 400

    # Imprimir en consola para verificar
    print(f"Actualización del índice del peer {peer_id}:")
    print(json.dumps(response_data, indent=4))

    return jsonify(response_data), 200



@app.route('/get_peers', methods=['GET'])
def get_peers():
    return jsonify(peers), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
