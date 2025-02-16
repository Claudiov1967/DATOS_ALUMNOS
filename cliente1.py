import socket
import sys
import binascii
import json

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def imprimir_lista(lista):
    """ 
    Imprime cada registro en un formato legible.

    Args:
        lista (list): Lista de registros a imprimir.

    Returns:
        None
    """
    for i, sublista in enumerate(lista, start=1):
        print(f"Registro {i}:")
        for j, valor in enumerate(sublista, start=1):
            print(f"  Elemento {j}: {valor}")
        print() 

# conectar al servidor
sock.connect((HOST, PORT)) 
# el mensaje que se enviara al servidor
mensaje = input("INTRODUZCA EL APELLIDO: ")

# Enviar el mensaje al servidor
sock.sendall(mensaje.encode('utf-8'))

# Recibir la respuesta del servidor
response = sock.recv(1024).decode('utf-8')
#print("Respuesta del servidor:", response)
respuesta_lista = json.loads(response)

# Llamar a la función para imprimir la lista
if respuesta_lista != []:
    imprimir_lista(respuesta_lista)
else:
    print("NO SE ENCONTRO EL APELLIDO")
# Cerrar la conexión
sock.close()
