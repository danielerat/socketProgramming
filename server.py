import socket
import threading
import sqlite3



#Variables for holding information about connections
connections = []
total_connections = 0

step=0
dataFor="email"
allDep=False

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            global allDep
            try:
                data = self.socket.recv(32)
                global step
                global dataFor
                
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("Client ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                if(str(data.decode("utf-8"))=="1" and step==0):
                    for client in connections:
                        if client.id == self.id:
                            subData="Enter the first and last name: "
                            client.socket.send(str.encode(subData))
                            step=1
                            dataFor="email"
                elif(str(data.decode("utf-8"))=="2" and step==0):
                    for client in connections:
                        if client.id == self.id:
                            subData="Enter the first and last name: "
                            client.socket.send(str.encode(subData))
                            step=1
                            dataFor="phoneNumber"
                elif(str(data.decode("utf-8"))=="3" and step==0):
                    for client in connections:
                        if client.id == self.id:
                            subData="Enter The Department Number:"
                            client.socket.send(str.encode(subData))
                            step=1
                            allDep=True
                            sqlite_select_query = "SELECT * from people  where dptNumber={}".format(data.decode("utf-8"))
                    
                else: 
                    name=list(str(data.decode("utf-8")).split(" ",1))
                    name.append("XXX") if len(name)<2 else ""
                    # if (str(data.decode("utf-8"))=="3"):sqlite_select_query = "SELECT * from people  where dptNumber={}".format(str(data.decode("utf-8")))
                    # else: 
                    if allDep:
                        sqlite_select_query = "SELECT * from people  where depNumber={}".format(str(data.decode("utf-8")))
                        allDep=False
                    else:
                        sqlite_select_query = "SELECT depNumber,firstName,lastName,{} from people where LOWER(firstName)=LOWER('{}') and lastName like '%{}%' ".format(dataFor,name[0],name[1])
                    
                    sqliteConnection = sqlite3.connect('Data.db')
            
                    cursor = sqliteConnection.cursor()

                    records = cursor.execute(sqlite_select_query).fetchall()
                    subSubData="----------\n"
                    for i in records:
                        subSubData+="DepId:{}\nNames:\n{}\nData:\n{}\n".format(str(i[0]),str(i[1]+" "+i[2]),str(i[3]))
                        subSubData+="\n----------\n"
                    print(subSubData)

                    for client in connections:
                        if client.id == self.id:
                            client.socket.send(str.encode(subSubData))
                            step=0

                       
                    
               
                # for client in connections:
                #     if client.id == self.id:
                #         client.socket.send(data)
                # Send to all connected client 
                # for client in connections:
                #     if client.id != self.id:
                #         client.socket.sendall(data)

#Wait for new connections
def newConnections(socket): 
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1
    
def main():
    #Get host and port
    host = input("Host: ")
    port = int(input("Port: "))
 
    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)


    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()