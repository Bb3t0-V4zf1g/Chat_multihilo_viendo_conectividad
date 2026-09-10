import socket, threading, json #import the modules to use sockets and threads

nicknames = {}

def send_message_to_all(message, sender):
    for client in nicknames.keys():
        if client != sender:  # Don't send the message back to the sender
            try:
                client.sendall(message.encode())
            except Exception as e:
                print(f"Error sending message to {nicknames.get(client)}: {e}") # Print any exceptions that occur while sending messages

def manage_client(conexion, cb):
    data = None
    try:
        # While loop to continuously receive data from the client until the connection is closed
        while True:
            # Receive data from the client
            received = conexion.recv(1024)
            # If no data is received, break the loop and close the connection
            if not received:
                break
            # Parse the received data as JSON
            data = json.loads(received.decode())

            if data["type"] == "register":
                # If the received data is a registration request, store the nickname of the client
                nicknames[conexion] = data["name"]
                conexion.sendall(f"Welcome {nicknames[conexion]}!".encode())

            elif data["type"] == "message":
                print(f"{nicknames.get(conexion)}: {data['message']}") # Print the received message from the client
                # Send a response back to the all the clients connected to the server
                cb(f"{nicknames.get(conexion)}: {data['message']}", conexion)
            elif data["type"] == "whois":
                # If the received data is a request for the list of connected clients, send the list back to the client
                connected_clients = [name for name in nicknames.values()]
                conexion.sendall(f"Connected clients: {', '.join(connected_clients)}".encode())
    except (ConnectionResetError, OSError) as e:
        # Handle the case where the client disconnects abruptly
        print(f"{nicknames.get(conexion)} disconnected abruptly: {e}")
    except ConnectionAbortedError as e:
        # Handle the case where the client aborts the connection
        print(f"{nicknames.get(conexion)} aborted the connection: {e}")
    finally:
        cb(f"{nicknames.get(conexion)} has left the chat.", conexion) # Send a message to all clients indicating that the client has left the chat
        try:
            # Remove the nickname of the disconnected client from the dictionary
            del nicknames[conexion] 
        except (KeyError, RuntimeError):
            pass
        finally:
            # Close the connection with the client
            conexion.close()

# Create a TCP socket and bind it to localhost on port 6000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 6000))

# Start listening for incoming connections with a backlog of 5
server.listen(5)
print("Server listening on port 6000...") # Print a message indicating that the server is listening for incoming connections

# Start an infinite loop to accept incoming connections and handle them in separate threads
while True:
    # Accept an incoming connection from a client
    conexion, address = server.accept()
    print(f"Somebody connected from {address}") # Print a message indicating that a connection has been established with the client
    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=manage_client, args=(conexion, send_message_to_all))
    # Start the client thread to handle the connection
    client_thread.start()
