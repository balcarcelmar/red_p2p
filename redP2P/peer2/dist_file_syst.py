# programa de python que se encarga de ejecutar un menú que contiene todas
# las funciones que puede realizar el peer como cliente del servicio

# importa el archivo del grpc client, que se encarga de la función de download
from file_transfer_client import download
# importa el archivo del peer correspondiente, incluyendo las funciones de comunicación con el servidor directorio
from peer2 import update_index, search_file_in_directory, get_index
import random

#meú de las opciones a las que puede acceder el programa
def menu():
    print("Que deseas hacer:")
    print("1. buscar archivo")
    print("2. actualizar indice de archivo")
    print("3. ver indice de archivos")
    print("4. descargar archivo")
    print("5. salir")



if __name__ == '__main__':
    print("bienvenido al sistema de archivos distribuido ")
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
            if peers_w_file:  
                peer_aleatorio = random.choice(peers_w_file)  # si el archivo de encuentra en varios peers, escoje aleatoreamente de cual peer hace la descarga
                ip = peer_aleatorio['peer_ip'] 
                download(file_name, ip)
                update_index() # se actualiza el índice del archivo cuando realiza la descarga
            else:
                print("No se pudo realizar la descarga.")
        elif opcion == 5:
            print("ha salido del sistema de archivos distribuido")
            break
        else :
            "ingresa una opción correcta"


