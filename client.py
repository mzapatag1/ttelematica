import socket              
  
port = 7070
server = socket.gethostbyname(socket.gethostname())
ct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ct.connect((server,port))

print (ct.recv(1024) ) 

ct.close()      
