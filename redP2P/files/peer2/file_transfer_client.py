import grpc
from concurrent import futures
import time
import os
import file_transfer_pb2
import file_transfer_pb2_grpc
 
def run():
    # Establecer la conexión con el servidor gRPC
    with grpc.insecure_channel('localhost:5000') as channel:
        stub = file_transfer_pb2_grpc.FileTransferStub(channel)
        
        # Llamada al método 'download' del servidor
        print("Realizando la descarga..")
        DownloadFile_request =file_transfer_pb2.FileRequest(file_name='finanzas.txt')
        DownloadFile_response = stub.DownloadFile(DownloadFile_request)

        print(DownloadFile_response.status)
        print(DownloadFile_response.file_content)
        
        #llamada al método de 'upload' del servidor
        print('Realizando la carga ..')
        UploadFile_request = file_transfer_pb2.FileRequest(file_name = 'casa2.txt', file_content= bytes('Hola soy juana',"utf-8"))
        UploadFile_response = stub.UploadFile(UploadFile_request)

        print(UploadFile_response.status)
        print(UploadFile_response.file_content)

if __name__ == '__main__':
    run()