import socket, json, threading

# Function to receive messages from the server in a separate thread
def receive_messages(client, name):
    while True:
        try:
            # Wait for a message from the server
            message = client.recv(1024)
            # If no message is received, it means the server has disconnected, so print a message and break the loop
            if not message:
                print("Servidor desconectado.")
                break
            print(f"\r\033[K{message.decode()}\n{name}: ", end="", flush=True) # Print the message and redraw the prompt
        except Exception:
            pass
            break

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server on localhost at port 6000
    client.connect(("localhost", 6000))

    # Prompt the user to enter a nickname
    name = input("Enter your nickname: ")

    # Send a registration request to the server with the nickname
    client.sendall(json.dumps({
        "type": "register",
        "name": name
    }).encode())

    # Receive the welcome before starting the thread and the input prompt
    print(client.recv(1024).decode())

    # Start a separate thread to receive messages from the server
    threading.Thread(
        target=receive_messages,
        args=(client, name),
        daemon=True
    ).start()

    # Main thread for sending messages
    while True:
        # Wait for user input to send a message to the server
        message = input(f"{name}: ")

        # If the user types 'exit', break the loop and close the connection
        if message.lower() == "/exit":
            print("Exiting the chat...")
            break
        if message.lower() == "/quienes":
            client.sendall(json.dumps({
                "type": "whois"
            }).encode())

        # Send the message to the server as a JSON object
        client.sendall(json.dumps({
            "type": "message",
            "message": message
        }).encode())

except KeyboardInterrupt:
    print("\nExiting the chat...")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection with the server
    client.close()