import socket
import tqdm

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('127.0.0.1',12345))
server.listen()

client, addr = server.accept()

file_size = int(client.recv(1024).decode())

client.sendall(("send file of size "+str(file_size)).encode())
file_name = "recvd.pdf"
file = open(file_name,"wb")

file_bytes = b""

while (len(file_bytes)<file_size):
    data = client.recv(1024)
    file_bytes+=data
    print(len(file_bytes))
   
file.write(file_bytes)
file.close()
client.close()
server.close()