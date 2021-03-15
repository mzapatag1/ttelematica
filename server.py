import socket

port = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 80))
s.listen(5)
s.bind(('localhost', port))     

print ("socket binded to %s" %(port))  
print ("socket is listening")             
  
while True:  
c, addr = s.accept()      
print ('Got connection from', addr ) 
  
# send a thank you message to the client.  
c.send('Thank you for connecting')  
  
# Close the connection with the client  
c.close()  
