import client
import socket

e, d, n = client.RSA_keygen(37,41)
ca_e, ca_n = 5, 437
client2 = client.Client((e, n), (d, n), (ca_e, ca_n), "ID1")
client2.get_publickey_ofclient("ID1")

print("Client 2's list: ",client2.map_pukeys, " ",client2.publickey_ca)

#communicate

s = socket.socket()        
port = 12345               
s.connect(('127.0.0.1', port))
print ("got from client 1", client2.receive(s.recv(1024).decode()))
s.send(client2.send('ack1',"ID1").encode())
print ("got from client 1", client2.receive(s.recv(1024).decode()))
s.send(client2.send('ack2',"ID1").encode())
print ("got from client 1", client2.receive(s.recv(1024).decode()))
s.send(client2.send('ack3',"ID1").encode())
s.close()    