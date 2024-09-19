import grpc
from concurrent import futures
import time
import os
import file_transfer_pb2
import file_transfer_pb2_grpc
import json

with open('./peer3_config.json', 'r') as config_file:
    config = json.load(config_file)

# Implementar el servicio gRPC
class FileTransferService(file_transfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request, context):
        file_name = request.file_name
        file_content = request.file_content
        with open(os.path.join(config['directory'], file_name), 'wb') as f:
            f.write(file_content)
        return file_transfer_pb2.FileResponse(status="Archivo subido exitosamente")
 
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
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
 
if __name__ == '__main__':
    serve()