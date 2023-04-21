import os
import socket
from rsa import *
import hashlib

def request_ca(id):
    client_socket = socket.socket()
    host = '127.0.0.1'
    port = 8765
    print('Waiting for connection response from CA')
    try:
        client_socket.connect((host, port))
    except socket.error as e:
        print(str(e))
    res = client_socket.recv(1024)
    print("Received from CA:", res.decode())

    client_socket.send(str.encode(id))
    res = client_socket.recv(1024).decode('utf-8')
    # print("got from server: ",res )
    client_socket.close()
    return res


def getkey_from_certificate(cert):
    ''' Client extracts public key of the other client from its certificate.
        Returns tuple of the form (e,n)
    '''
    decrypted_msg = RSA_decrypt_string(cert, publickey_ca)
    print("Getting key from certificate:")
    print(decrypted_msg)
    
    contents=decrypted_msg.split("::")
    key = contents[1]
    key = key.split(',')
    key[0]=int(key[0][1:])
    key[1]=int(key[1][:-1])
    return (key[0],key[1])


def request( name, rollno, PR_user,publickey_ca,PU_server):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("127.0.0.1",12345))

    # send name, rollno to the server
    request_msg = (name + "," + rollno)
    request_msg_hash = request_msg+','+hashlib.sha256(request_msg.encode()).hexdigest()
    encrypted_msg = RSA_encrypt_string(request_msg_hash,PU_server)
    client.sendall(encrypted_msg.encode())
    

    # receive the encrypted msg from server
    msg = client.recv(1024).decode()
    print("Received from Server:", msg)
    if((msg == "NAME AND ROLLNO NOT FOUND")or(msg=="INTEGRITY FAILURE")):
        return 
    
    encmsg_size = int(client.recv(1024).decode())
    client.send(("Received len: "+str(encmsg_size)).encode())
    enc_msg = b""

    while (len(enc_msg)<encmsg_size):
        data = client.recv(1024)
        enc_msg+=data

    print("Final message size:", len(enc_msg))    
    

    # decrypt the msg
    msg = RSA_decrypt_bytes(enc_msg.decode(), PR_user)
    s1 = int.from_bytes(msg[0:4], byteorder='little')
    s2 = int.from_bytes(msg[4:8], byteorder='little')
    s3 = int.from_bytes(msg[8:12], byteorder='little')
    s4 = int.from_bytes(msg[12:16], byteorder='little')

    print("size of PDF1:", s1)
    print("size of PDF2:", s2)
    print("size of encryptedhash1:", s3)
    print("size of encryptedhash2:", s4)
    print("\n\n")
    
    PDF1 = msg[16:16+s1]
    PDF2 = msg[16+s1:16+s1+s2]
    PDFs = PDF1+PDF2
    encryptedhash1 = msg[16+s1+s2:16+s1+s2+s3]
    encryptedhash2 = msg[16+s1+s2+s3:16+s1+s2+s3+s4]

    curtime = msg[16+s1+s2+s3+s4:].decode()

    print("TIME: ",curtime)

    # request certificate of Director from CA
    Cert_dir = request_ca("Director")
    PU_dir = getkey_from_certificate(Cert_dir)
    print("\n\n")

    # authenticate Director
    hash1 = hashlib.sha256(PDFs).hexdigest()
    print("received hash1:", hash1)
    print("received encryptedhash1:", encryptedhash1.decode())
    found_hash1 = RSA_decrypt_string(encryptedhash1.decode(), PU_dir)
    print("Digital signature of Director matched ", hash1 == found_hash1)
    print("\n\n")

    # request certificate of Registrar from CA
    Cert_reg = request_ca("Registrar")
    PU_reg = getkey_from_certificate(Cert_reg)
    print("\n\n")

    # authenticate Registrar
    hash2 = hashlib.sha256(PDFs).hexdigest()
    print("received hash2:", hash2)
    print("received encryptedhash2:", encryptedhash2.decode())
    found_hash2 = RSA_decrypt_string(encryptedhash2.decode(), PU_reg)
    print("Digital signature of Registrar matched ", hash2 == found_hash2)
    print("\n\n")


    # save the PDFs 
    file_name = "recvd_degree.pdf"
    file = open(file_name, "wb")
    file.write(PDF1)
    file.close()

    file_name = "recvd_grades.pdf"
    file = open(file_name, "wb")
    file.write(PDF2)
    file.close()
     
    # close the connection
    client.close()
     
     

if __name__ == "__main__":
    publickey_ca = (5, 437)
    print("Keys for the 3 students")
    print(RSA_keygen(53, 59))
    print(RSA_keygen(61, 67))
    print(RSA_keygen(71, 73))
    print("\n\n")

    Cert_server = request_ca("Server")
    PU_server = getkey_from_certificate(Cert_server)
    request("Person1", "2019215", (2011, 3127),publickey_ca,PU_server)
    # request("Person2", "2019216", (2263, 4087),publickey_ca,PU_server)
    # request("Person3", "2019217", (2291, 5183),publickey_ca,PU_server)
    

   


