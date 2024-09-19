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
        
        print("Realizando la descarga..")
        UploadFile_request =file_transfer_pb2.FileRequest(file_name='archivo1.txt',file_content=bytes())
        uploadFile_response = stub.DownloadFile(UploadFile_request)

        print(uploadFile_response.status)
        print(uploadFile_response.file_content)
        

if __name__ == '__main__':
    run()