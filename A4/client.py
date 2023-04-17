import os
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",12345))

file = open("grades.pdf","rb")
file_size = os.path.getsize("grades.pdf")
print(file_size)

client.sendall(str(file_size).encode())
print(client.recv(1024).decode())
data = file.read()
# print(data[0])
client.sendall(data)


file.close()
client.close()

