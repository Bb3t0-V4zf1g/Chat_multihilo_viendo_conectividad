import socket, json, threading # importar los modulos

# Funcion para recibir mensajes del servidor
def receive_messages(client, name):
    while True:
        try:
            # Esperar a recibir un mensaje del servidor
            message = client.recv(1024)
            # Si no se recibe ningún mensaje, significa que el servidor se ha desconectado, por lo que se rompe el bucle
            if not message:
                print("Servidor desconectado.")
                break
            # Imprimir el mensaje recibido 
            # \r para mover el cursor en la linea actual sin pasar a la siguiente linea
            # \033 es "esc" en código ASCII y esto evita que queden restos de texto antiguo en pantalla. Desde el cursor hasta el final de la linea
            # \n Después de imprimir el mensaje recibido, pasa a la siguiente línea.
            # end= "" evita un salto de linea adicional
            # flush, Fuerza a que la salida se muestre inmediatamente en pantalla.
            print(f"\r\033[K{message.decode()}\n{name}: ", end="", flush=True) 
        except Exception:
            pass
            break

# Crear un socket por parte del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conectar el cliente al localhost y puerto 6000
    client.connect(("localhost", 6000))

    # Input para recibir por parte dle usuario un nombre o apodo
    name = input("Enter your nickname: ")

    # Enviar un mensaje de tipo regirtro para que el servidor lo reconozca por su apodo o nombre esta conexión
    client.sendall(json.dumps({
        "type": "register",
        "name": name
    }).encode())

    # Imprimir lo que el servidor le envía al cliente
    print(client.recv(1024).decode())

    # Iniciar un hilo en donde se ejecuta en segundo plano para recibir cada mensaje que el servidor le envía a esta conexión
    threading.Thread(
        target=receive_messages,
        args=(client, name),
        daemon=True
    ).start()

    # Hilo principal para envíar mensajes al servidor sin limites
    while True:
        # Esperar a que el cliente ingrese su mensaje a enviar
        message = input(f"{name}: ")

        # Si el cliente ingresa "/exit" se desconecta
        if message.lower() == "/exit":
            print("Exiting the chat...")
            break

        # Si el cliente ingresa "/quienes" se le retorna una lista de los clientes conectados
        if message.lower() == "/quienes":
            client.sendall(json.dumps({
                "type": "whois"
            }).encode())

        # Enviar el mensaje del cliente en JSON al servidor y el servifor lo envía a todos los clientes conectados
        client.sendall(json.dumps({
            "type": "message",
            "message": message
        }).encode())

# Manejar la salida por ctrl + C
except KeyboardInterrupt:
    print("\nExiting the chat...")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Cerrar la conexión del cliente
    client.close()