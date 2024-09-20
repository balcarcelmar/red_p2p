import grpc
from concurrent import futures
import time
import os
import file_transfer_pb2
import file_transfer_pb2_grpc
import json
 
# archivo de configuración
with open('./peer3_config.json', 'r') as config_file:
    config = json.load(config_file)

#funcion de descarga de archivo
def download(fileName,ip):
    # Establecer la conexión con el servidor gRPC
    with grpc.insecure_channel(ip) as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)

        # Llamada al método 'download' del servidor
        print("Realizando la descarga..")
        DownloadFile_request =file_transfer_pb2.FileRequest(file_name=fileName)
        DownloadFile_response = stub.DownloadFile(DownloadFile_request)

        if(DownloadFile_response.status=="Archivo descargado"):
            with open(os.path.join(config['directory'], fileName), 'wb') as f:
                f.write(DownloadFile_response.file_content)

        print(DownloadFile_response.status)
    return 