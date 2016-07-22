import socket,sys,thread,threading,time
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def msg_recv():
    while 1:
        data = client_socket.recv(4096)
        if str(data) == "file in coming":
            print "file in coming\n"
            #k = raw_input('accept?  (Y/n)\n')
            #if str(k)!='n':
            #print str(data)+"\n" 
            with open('received_file', 'wb') as f:
                print 'file opened'
                while True:
                    print('receiving data...')
                    data = client_socket.recv(4096)
                    #print('data=%s', (data))
                    if not data or data == 'done':
                        break
                    # write data to a file
                    f.write(data)
                    #break
            print "done.\n"
            f.close()
            
        elif data:
            print (data)+"\n"
def msg_send():
    print "send / kick / ls / chat ..... or 'help' for above command\n"
    while 1:
        a = raw_input("Type : (global channel Default)\n")
        if a == 'q':
            print "leave"
            client_socket.shutdown(1)
            client_socket.close()
            sys.exit()
        elif a == 'send':
            cmd = raw_input("type filename / type 'q' to abort : \n")
            if cmd == 'q':
                print "alright then."
            else:
                filename = str(cmd)
                f = open(filename,'rb')
                l = f.read(1024)
                receiver = int(raw_input("type receiver ID : \n"))
                client_socket.send("send "+str(receiver))
                time.sleep(1)
                while (l):
                    client_socket.send(l)
                    print('Sent ',repr(l))
                    l = f.read(1024)
                f.close()
                time.sleep(1)
                client_socket.send('done')
        elif a == 'help':
            print "send / kick / ls / chat"
        elif a == 'kick':
            user = raw_input("type user you want to kick\n")
            client_socket.send("kick "+str(user))  
        elif a == "chat":
            user = raw_input("type user you want to talk to\n")
            msg =  raw_input("type message you want to send\n")
            client_socket.send("chat "+str(user)+" "+str(msg)) 
        else :
            client_socket.send(a)
def chat_client():
    IP = raw_input("type IP addr:\n")
    client_socket.connect((IP, 5000))
    print "HII~\n"
    client_socket.send("somebody in")
    try:
        t = Thread(None,msg_recv,None,())
        t2 = Thread(None,msg_send,None,())
        t.start()
        t2.start()
        t.join()
        t2.join()
    except Exception as errtxt:
        print "!"+str(errtxt)
     

if __name__ == "__main__":
    sys.exit(chat_client())
while 1:
    pass
