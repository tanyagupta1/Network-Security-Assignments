import socket
import os
from _thread import *

from math import gcd
import itertools
from datetime import datetime
from dateutil.relativedelta import relativedelta

from rsa import RSA, RSA_encrypt_string, RSA_decrypt_string, RSA_keygen

 

class CA:
  id_iter = itertools.count()

  def __init__(self, pu, pr):
    self.map_pukeys = {}
    self.privatekey = pr
    self.id = next(self.id_iter)
  
  def get_certificate(self, client):
    ''' returns encrypted certificate which has PU of client'''

    # (IDA, PUA, TA, DURA, IDCA)
    # DURA is in years
    PUA = self.map_pukeys[client]
    TA = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # TA = str(datetime.date(1970,1,1)) 
    DURA = 5
    cert_contents = [client, PUA,TA,DURA, self.id]
    msg=""
    for c in cert_contents:
      msg+="::"+str(c)
    msg=msg[2:]
    enc_msg=RSA_encrypt_string(str(msg),self.privatekey)
    return enc_msg

  def add_publickey(self, id_client, key):
    self.map_pukeys[id_client] = key 

  def handle_client(self, connection):
      connection.send(str.encode('Server is working:'))
      data = connection.recv(2048)
      m = data.decode('utf-8')
      print("Server received: ",m)
      response = self.get_certificate(m)
      print("sending response: ", response)
      connection.sendall(str.encode(response))
      connection.close()



if __name__ == "__main__":

  ca_e, ca_d, ca_n = RSA_keygen(19, 23)
  CA_obj = CA((ca_e, ca_n), (ca_d, ca_n)) # keys were self created. We chose p,q ensuring n > 255
  
  print("public key of CA ",(ca_d, ca_n))  #(317, 437)

  e, d, n = RSA_keygen(29, 31)
  print("private key of University Authority ",(e, n))  #(11, 899)
  CA_obj.add_publickey("UniversityAuthority", (d, n))
  
  e, d, n = RSA_keygen(37, 41)
  print("private key of Director ",(e, n))  #(7, 1517)
  CA_obj.add_publickey("Director", (d, n))
  
  e, d, n = RSA_keygen(43, 47)
  print("private key of Registrar ",(e, n))  #(5, 2021)
  CA_obj.add_publickey("Registrar", (d, n))


  server_socket = socket.socket()
  host = '127.0.0.1'
  port = 8765
  ThreadCount = 0
  try:
      server_socket.bind((host, port))
  except socket.error as e:
      print(str(e))
  print('Socket is listening..')
  server_socket.listen(5)


  while True:
      Client, address = server_socket.accept()
      print('Connected to: ' + address[0] + ':' + str(address[1]))
      start_new_thread(CA_obj.handle_client, (Client, ))
      
      
  server_socket.close()
 