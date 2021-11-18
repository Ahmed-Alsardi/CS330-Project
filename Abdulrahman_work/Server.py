import socket
						

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Server in Passive Mode - Listening")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))



s.bind(("localhost", 9999))
s.listen(1)
while True:
    conn, addr = s.accept() #accept connection
    print ("New Client Accepted",addr)
    name = conn.recv(1024).decode() #recive mood from client
    if name == '1' :
        conn.send(bytes("open mode ready","utf-8")) #inform client by mood
        while True:
            r = conn.recv(1024).decode()#recive client msg
            if r == "bye":
                break
            print("message from client: "+r) #print client msg
            recive_user = input("Enter your msg to client: ") #msg from user
            conn.send(bytes(recive_user,"utf-8")) # send user msg to client
    conn.close()
    break
    


                    