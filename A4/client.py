import os
import socket
import rsa

e, d, n = rsa.RSA_keygen(19, 23)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",12345))

file = open("grades.pdf","rb")
data = file.read()

enc_file = rsa.RSA_encrypt_string(data,(e,n)).encode()

file_size = len(enc_file)
print(file_size)

client.sendall(str(file_size).encode())
print(client.recv(1024).decode())

client.sendall(enc_file)




file.close()
client.close()


