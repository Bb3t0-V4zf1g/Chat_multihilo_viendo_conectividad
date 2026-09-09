import socket, threading #import the modules to use sockets and threads

def handle_client(conexion, address):
    try:
        # While loop to continuously receive data from the client until the connection is closed
        while True:
            # Receive data from the client
            data = conexion.recv(1024)
            # If no data is received, break the loop and close the connection
            if not data:
                break
            print(f"Received from {address}: {data.decode()}") # Confirmation message that the server received data from the client
            # Send a response back to the client
            conexion.sendall(f"Server received: {data.decode()} from {address}".encode())
    except ConnectionResetError as e:
        # Handle the case where the client disconnects abruptly
        print(f"The client {address} disconnected abruptly: {e}")
    except ConnectionAbortedError as e:
        # Handle the case where the client aborts the connection
        print(f"The client {address} aborted the connection: {e}")
    finally:
        print(f"Closing connection with {address}") # Print a message indicating that the connection with the client is being closed
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
    print(f"Connection established with {address}")
    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(conexion, address))
    # Start the client thread to handle the connection
    client_thread.start()