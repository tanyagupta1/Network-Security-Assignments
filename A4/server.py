import socket
import rsa

class Server:

    def authenticate_client():
        pass

    def respond():
        pass

    def signUA():
        "hash the doc and encrypt hash using PR of University Authority"
        pass

    def signRegistrar():
        "hash the doc and encrypt hash using PR of Registrar"
        pass

    def signDirector():
        "hash the doc and encrypt hash using PR of Director"
        pass

    def putdatetime():
        pass

    def watermark():
        pass

if __name__ == "__main__":
    e, d, n = rsa.RSA_keygen(19, 23)

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

    # print(file_bytes)
    file_bytes = rsa.RSA_decrypt_string(file_bytes.decode(),(d,n))

    # print(file_bytes)
    file.write(file_bytes)
    file.close()
    client.close()
    server.close()