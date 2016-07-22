import socket, select,thread,time,sys
from threading import Thread
CONNECTION_LIST = []
DELETE_LIST = ""
RECV_BUFFER = 4096
PORT = 5000
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
def broadcast(sock,msg):
    try :
        sock.send(msg)
    except :
        sock.close()
        CONNECTION_LIST.remove(sock)
def lists():
    tmp = ""
    i=0
    for sock in CONNECTION_LIST:
        #print CONNECTION_LIST[0]
        if sock == server_socket:
            tmp += "[SERVER]  >>  "+str(sock)+"\n"
        else:
            tmp+= str(i)+"  >>  "+str(sock)+"\n"
        i+=1
    return tmp
    
def auto():
    global DELETE_LIST
    while 1:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr               
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
            elif sock ==  DELETE_LIST:
                broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                print "Client (%s, %s) is offline" % addr
                sock.close()
                CONNECTION_LIST.remove(sock)
                DELETE_LIST = ""
                continue
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    data_split = data.split(' ')
                    if data=="ls":
                        print "df"
                        print str(sock.getpeername())+" ask for list\n"
                        broadcast(sock,lists())
                        print lists()
                    elif data_split[0] ==  'send':    # send file receiver
                        try:
                            t = Thread(None,sending,None,(sock,int(data_split[1])))
                            t.start()
                            t.join()
                        except Exception as err:
                            print str(err)
                            broadcast(sock,"somthing wrong\n")
                    elif data_split[0] == 'kick':
                        try:
                            user = int(data_split[1])
                            broadcast(CONNECTION_LIST[user],"someone kick you .... QQ\n")
                            broadcast_data(CONNECTION_LIST[user],"someone kick "+str(CONNECTION_LIST[user])+ "  .... QQ\n")
                            DELETE_LIST = CONNECTION_LIST[user]
                        except Exception as err:
                            print str(err)
                            broadcast(sock,"somthing wrong\n")
                    elif data_split[0] == 'chat':
                        try:
                            user = int(data_split[1])
                            msg = str(data_split[2])
                            broadcast(CONNECTION_LIST[user],"Message from "+str(sock)+"\n")
                            broadcast(CONNECTION_LIST[user],msg);
                        except Exception as err:
                            print str(err)
                            broadcast(sock,"somthing wrong\n")
                    elif data:
                        print str(sock.getpeername())+data+"\n"
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                except Exception as errtxt:
                    print errtxt
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
           
     
    server_socket.close()
def sending(sock,recv):
    tmp = ''
    print "file in coming\n"
    CONNECTION_LIST[recv].send('file in coming')
    time.sleep(1)
    with open('received_file_server', 'wb') as f:
        print 'file opened'
        while True:
            print('receiving data...')
            data = sock.recv(4096)
            #print('data=%s', (data))
            if not data or data == 'done':
                break
            print('sending data...')
            CONNECTION_LIST[recv].send(data)
            # write data to a file
            f.write(data)
            #break
    print "done.\n"
    time.sleep(1)
    CONNECTION_LIST[recv].send('done')
    f.close()


def command():
    global DELETE_LIST
    while 1:
        a = raw_input("waiting your command:\n")
        if a == "ls":
            print CONNECTION_LIST
        elif a == "kick":
            i = 0
            for sock in CONNECTION_LIST:
                #print CONNECTION_LIST[0]
                if sock == server_socket:
                    print "[SERVER]  >>  "+str(sock)
                else:
                    print str(i)+"  >>  "+str(sock)
                i+=1
            cmd = raw_input("type num to kick / type 'q' to abort : \n")
            if cmd == 'q':
                print "alright then."
                
            else:
                try:
                    cmd = int(cmd)
                    broadcast_data(server_socket, "uh .. someone 888888")
                    DELETE_LIST = CONNECTION_LIST[cmd]
                    print "kick "+str(cmd)
                except Exception as errtxt:
                    print errtxt
        elif a =="send":
            i=0
            for sock in CONNECTION_LIST:
                #print CONNECTION_LIST[0]
                if sock == server_socket:
                    print "[SERVER]  >>  "+str(sock)
                else:
                    print str(i)+"  >>  "+str(sock)
                i+=1
            cmd = raw_input("type filename / type 'q' to abort : \n")
            if cmd == 'q':
                print "alright then."
            else:
                filename = str(cmd)
                f = open(filename,'rb')
                l = f.read(1024)
                receiver = int(raw_input("type receiver ID : \n"))
                CONNECTION_LIST[receiver].send("file in coming")
                time.sleep(1)
                while (l):
                    CONNECTION_LIST[receiver].send(l)
                    print('Sent ',repr(l))
                    l = f.read(1024)
                f.close()
                    
def chat_server():
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("192.168.1.112", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    print "Chat server started on port " + str(PORT)
    try:
        t = Thread(None,auto,None,())
        t2 = Thread(None,command,None,())
        t.start()
        t2.start()
        t.join()
        t2.join()
    except Exception as errtxt:
        print errtxt
if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sys.exit(chat_server())
while 1:
    pass

    
    


