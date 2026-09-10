import socket, threading, json #importar modulos

# Diccionario que guardar como clave la conexion y como valor el nickname del cliente
nicknames = {}

def send_message_to_all(message, sender):
    # Recorrer cada cliente conectado y enviar el mensaje a todos excepto al remitente
    for client in nicknames.keys():
        if client != sender:  # Menos al remitente
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message to {nicknames.get(client)}: {e}") # Imprimir un mensaje de error 

def manage_client(conexion, cb):
    # Variable para almacenar los datos recibidos del cliente
    data = None
    try:
        # Bucle para seguir recibiendo datos del cliente mientras la conexión esté activa
        while True:
            # Recibe los datos del cliente en bytes
            received = conexion.recv(1024)
            # Si no se reciben datos, significa que el cliente ha cerrado la conexión, por lo que se rompe el bucle
            if not received:
                break
            # Decodifica los datos recibidos de bytes a string y luego los carga como un objeto JSON
            data = json.loads(received.decode())

            if data["type"] == "register":
                # Si el tipo de datos recibido es "register", se guarda el cliente enel diccionario de nicknames 
                nicknames[conexion] = data["name"]
                conexion.sendall(f"Welcome {nicknames[conexion]}!".encode()) # Se envía un mensaje de bienvenida al cliente

            elif data["type"] == "message":
                print(f"{nicknames.get(conexion)}: {data['message']}") # Imprimir el mensaje recibido del cliente en la consola del servidor
                # Enviar el mensaje a todos los clientes conectados excepto al remitente
                cb(f"{nicknames.get(conexion)}: {data['message']}", conexion)

            elif data["type"] == "whois":
                # Si el tipo de datos recibido es "whois", se envía al cliente una lista de todos los clientes conectados
                connected_clients = [name for name in nicknames.values()]
                conexion.sendall(f"Connected clients: {', '.join(connected_clients)}".encode())
    except (ConnectionResetError, OSError) as e:
        # Manejar el caso donde el cliente cierra la conexión abruptamente
        print(f"{nicknames.get(conexion)} disconnected abruptly: {e}")
    except ConnectionAbortedError as e:
        # Manejar el caso donde la conexión es abortada
        print(f"{nicknames.get(conexion)} aborted the connection: {e}")
    finally:
        # Notificar a todos los clientes que el cliente se ha desconectado
        cb(f"{nicknames.get(conexion)} has left the chat.", conexion) 
        try:
            # Remover el cliente del diccionario de nicknames cuando se desconecta
            del nicknames[conexion] 
        except (KeyError, RuntimeError):
            # Manejar cuando el diccionario es modificado mientras los clientes están siendo iterados
            pass
        finally:
            # Cerrar la conexión con el cliente
            conexion.close()

# Crear un socket TCP para el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configurar el socket para conectar a la dirección 'localhost' en el puerto 6000
server.bind(('localhost', 6000))

# El servidor comienza a escuchar conexiones entrantes en el puerto especificado
server.listen()
print("Server listening on port 6000...") # Imprimir un mensaje indicando que el servidor está escuchando en el puerto 6000

# Empezar un bucle infinito para aceptar conexiones entrantes de clientes
while True:
    # Aceptar una conexión entrante de un cliente
    conexion, address = server.accept()
    print(f"Somebody connected from {address}") # Imprimir un mensaje indicando que se ha establecido una conexión con el cliente
    # Crear un hilo para manejar la conexión del cliente, pasando la función manage_client y los argumentos necesarios
    client_thread = threading.Thread(target=manage_client, args=(conexion, send_message_to_all))
    # Empezar el hilo para manejar la conexión del cliente
    client_thread.start()
