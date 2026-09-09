import socket

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server on localhost at port 6000
client.connect(('localhost', 6000))

# Start an infinite loop to send messages to the server with the same socket connection
while True:
    # Wait for user input to send a message to the server
    message = input("Enter a message to send to the server: ")

    # If the user types 'exit', break the loop and close the connection
    if message.lower() == 'exit':
        break

    # Send the message to the server
    client.sendall(message.encode())

    # Receive a response from the server
    response = client.recv(1024)
    print(f"Received from server: {response.decode()}") # Print the response received from the server

# Close the connection with the server
client.close()
