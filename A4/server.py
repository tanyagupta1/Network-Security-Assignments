import socket
from rsa import *
from _thread import *
import time
import hashlib

def handle_client(connection):
    
    # verify that name and rollno are indeed present in DB
    msg = connection.recv(1024).decode()
    print("Received:", msg)
    print("\n\n")
    name, rollno = msg.split(",")
    if((name,rollno) not in DB):
        connection.sendall("NAME AND ROLLNO NOT FOUND".encode())
        connection.close()
        return 
    connection.sendall("SUCCESS".encode())

    # obtain the PDFs
    degree , grade, PU_user = DB[(name,rollno)]
    file = open(degree,"rb")
    PDF1 = file.read()
    file.close()

    file = open(grade,"rb")
    PDF2 = file.read()
    file.close()

    # add watermark to each


    # put date and time


    # concatenate the two PDFs
    PDFs = PDF1 + PDF2

    # hash the doc and encrypt hash using PR of Registrar
    hash1 = hashlib.sha256(PDFs).hexdigest()
    print("sent hash1:", hash1)
    encryptedhash1 = RSA_encrypt_string(hash1, (7, 1517)).encode()
    print("sent encryptedhash1:", encryptedhash1.decode())
    print("\n\n")


    # hash the doc and encrypt hash using PR of Director
    hash2 = hashlib.sha256(PDFs).hexdigest()
    print("sent hash2:", hash2)
    encryptedhash2 = RSA_encrypt_string(hash2, (5, 2021)).encode()
    print("sent encryptedhash2:", encryptedhash2.decode())
    print("\n\n")


    # Attach the 2 hashes to the PDFs
    # first 4 fields will be 4 byte each
    print("size of PDF1:", len(PDF1))
    print("size of PDF2:", len(PDF2))
    print("size of encryptedhash1:", len(encryptedhash1))
    print("size of encryptedhash2:", len(encryptedhash2))
    print("\n\n")
    msg = len(PDF1).to_bytes(4,'little')+len(PDF2).to_bytes(4,'little') + len(encryptedhash1).to_bytes(4,'little') + len(encryptedhash2).to_bytes(4,'little') + PDFs + encryptedhash1 + encryptedhash2
    

    # encrypt for confidentiality
    enc_msg = RSA_encrypt_bytes(msg, PU_user).encode()
    

    # send the final message to client
    encmsg_size = len(enc_msg)
    connection.sendall(str(encmsg_size).encode())
    print("Final message size:", encmsg_size)
    connection.sendall(enc_msg)
    

    # close the connection
    connection.close()
  
    


if __name__ == "__main__":
    
    # filling DB map
    
    DB = {}
    DB[("Person1", "2019215")] = ("db\Person1_degree.pdf", "db\Person1_grades.pdf", (3, 3127))
    DB[("Person2", "2019216")] = ("db\Person2_degree.pdf", "db\Person2_grades.pdf", (7, 4087))
    DB[("Person3", "2019217")] = ("db\Person3_degree.pdf", "db\Person3_grades.pdf", (11, 5183))

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print('Socket is listening...')
    server_socket.listen(5)

    # while True:
    Client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(handle_client, (Client, ))
    time.sleep(10) 
        
    
   
     

     

    