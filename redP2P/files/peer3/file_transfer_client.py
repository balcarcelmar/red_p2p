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
def download(fileName):
    # Establecer la conexión con el servidor gRPC
    with grpc.insecure_channel(f'{config['ip']}:{config['port']}') as channel:
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

#función de carga de archivos
def upload(fileName):
    file_path = os.path.join(config['directory'], fileName)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
    else:
        print('Archivo no encontrado')
        return 
 
    # Establecer la conexión con el servidor gRPC
    with grpc.insecure_channel(f'{config['ip']}:{config['port']}') as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        
        #llamada al método de 'upload' del servidor
        print('Realizando la carga ..')
        UploadFile_request = file_transfer_pb2.FileRequest(file_name = fileName, file_content= content)
        UploadFile_response = stub.UploadFile(UploadFile_request)

        print(UploadFile_response.status)
    return 
