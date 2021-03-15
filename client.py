import socket              
  
port = 80 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))  
  
# receive data from the server  
print (s.recv(1024) ) 
# close the connection  
s.close()      