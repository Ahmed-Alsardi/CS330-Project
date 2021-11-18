import socket
					
try:
    s = socket.socket()
    print ("Connection to server IP: "+ "localhost")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

s.connect(("localhost",9999)) #request conection
while True:
    name = input("Select one of the option : \n 1) open mode \n 2) secure mode \n 3) quit mode \n")

    if name == "1" or 1: #determine mood
        s.send(bytes("1","utf-8")) #send mood to server
        server_message = s.recv(1024).decode() #recive server mood response
        if server_message == "open mode ready": 
            print("you are in open mood enter your message: ")
            while True:
                recive_user = input("Enter your msg to server: ") # msg from user
                if recive_user == "bye":
                    s.send(bytes(recive_user,"utf-8"))# close server connection
                    break #stop 
                s.send(bytes(recive_user,"utf-8")) #send msg to server
                r= s.recv(1024).decode() #recive server msg
                print("message from server: "+ r) #print server msg

    break




