# programa que corre el servicio de grpc para las funcioes download y upload. 
import grpc
from concurrent import futures
import time
import os
import file_transfer_pb2
import file_transfer_pb2_grpc
import json
# se importa del archivo que maneja las funciones de conexión con el servidor directorio, login y logout
from peer2 import login, logout

#archivo de configuración
with open('./peer2_config.json', 'r') as config_file:
    config = json.load(config_file)

# Implementar el servicio gRPC
class FileTransferService(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request, context):
        file_name = request.file_name
        file_content = request.file_content
        with open(os.path.join(config['directory'], file_name), 'wb') as f:
            f.write(file_content)
        return file_transfer_pb2.FileResponse(status="Archivo subido exitosamente")
    
 # definición de la función de download
    def DownloadFile(self, request, context):
        file_name = request.file_name
        file_path = os.path.join(config['directory'], file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            return file_transfer_pb2.FileResponse(file_content=content, status="Archivo descargado")
        else:
            return file_transfer_pb2.FileResponse(status="Archivo no encontrado")
 
# Inicializar servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferService(), server)
    server.add_insecure_port(f"{config['ip']}:{config['port']}")
    login()  # se hace el login en el servidor directorio cuando al momento que se inicia el servidor de grpc
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        logout() # si el servidor grpc se interrumpe se hace la función de logut hacia el servidor directorio
 
if __name__ == '__main__':
    serve()