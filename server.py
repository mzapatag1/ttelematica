import socket

port = 7070
server = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))
s.listen(5)


print ("socket binded to %s" %(port))  
print ("socket is listening")             
  
while True:  
    c, addr = s.accept()      
    print ('Got connection from', addr ) 
