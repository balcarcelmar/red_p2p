from file_transfer_client import download
from peer2 import login, logout, update_index, search_file_in_directory, get_index
import random
import subprocess

def menu():
    print("bienvenido al sistema de archivos distribuido.Que deseas hacer: ")
    print("1. buscar archivo")
    print("2. actualizar indice de archivo")
    print("3. ver indice de archivos")
    print("4. descargar archivo")
    print("5. salir")



if __name__ == '__main__':
    login()
    proceso = subprocess.Popen(['python', './file_transfer_service.py'])
    while True:
        menu()
        opcion= int(input("ingresa el número de la opción seleccionada:"))
        if opcion == 1:
            file_name= input("ingresa el nombre del archivo que quieres buscar: ")
            search_file_in_directory(file_name)
        elif opcion == 2:
            update_index()
        elif opcion == 3:
            get_index()
        elif opcion == 4:
            file_name= input("ingresa el nombre del archivo que quieres descargar: ")
            peers_w_file = search_file_in_directory(file_name)
            peer_aleatorio = random.choice(list(peers_w_file))
            ip = peers_w_file[peer_aleatorio]['peer_ip']
            download(file_name,ip)
        elif opcion == 5:
            print("ha salido del sistema de archivos distribuido")
            logout()
            break
    proceso.terminate()


