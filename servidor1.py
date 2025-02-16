import socket
import socketserver
import binascii
from datetime import datetime
import sqlite3
import json
from icecream import ic

global PORT


class MyTCPHandler(socketserver.BaseRequestHandler):
      """
    Clase MyTCPHandler que maneja las solicitudes TCP.

    Methods:
        handle(): Maneja la solicitud recibida del cliente.
    """
    def handle(self):
        """
        Maneja la solicitud recibida del cliente.

        Recibe datos del cliente, decodifica el apellido y consulta la base de datos para obtener información del alumno. Envía la información al cliente en formato JSON.

        Args:
            None

        Returns:
            None
        """
        ic("hola 1")
        client_address = self.client_address[0]
        client_port = self.client_address[1]
        ic(f"Conectado a puerto: {client_port} y address: {client_address}")
        
        data = self.request.recv(1024).strip()

        try:
            apellido = data.decode('utf-8')
            ic("Datos recibidos:", apellido)
            ic(type(apellido))
        except UnicodeDecodeError:
            # Si no se puede decodificar como ASCII, se asume que es hexadec
            binary_field = bytearray(data)
            ic("Si viene como bytearray")
            ic("Valor recibido: ", binascii.hexlify(binary_field).decode("utf-8"))
            apellido = binascii.unhexlify(data).decode('utf-8')
            ic("Apellido decodificado desde hexadecimal:", apellido)
                       
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect("escuela.db")
            cursor = conn.cursor()
            apellido=apellido.lower()

            # Consultar la base de datos
            cursor.execute("SELECT * FROM Alumno2 WHERE LOWER(apellido) =?", (apellido,))
            result = cursor.fetchall()
            ic(result)
            # Convertir el resultado a una cadena JSON
            resultado_json = json.dumps(result)
            # Enviar una respuesta al cliente
            self.request.sendall(resultado_json.encode('utf-8'))

            # Cerrar la conexión a la base de datos
            conn.close()
        
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
           
 
if __name__ == "__main__":
    """
    Inicializa el servidor TCP.

    Este bloque de código inicializa una instancia de `TCPServer`, pasando `HOST` y `PORT`, y comienza a escuchar las solicitudes entrantes.

    Attributes:
        HOST (str): Dirección del host.
        PORT (int): Puerto en el que el servidor escucha.

    Returns:
        None
    """
    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        ic(f"Servidor lanzado y escuchando en {HOST}:{PORT}")
        server.serve_forever()
