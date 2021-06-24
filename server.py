import socket
import threading
import pickle
import uuid#generate unique id
from message import Message
# ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine
# this error occurs if you close socket too early
class Server(threading.Thread):
    clients = []
    ids= []
    def run(self):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind(('localhost', 8080))
        serv.listen(5)
        while True:
            conn, addr = serv.accept()
            connection = Connection(conn, addr)
            unique = uuid.uuid4().int
            self.clients.append(connection)
            self.ids.append(unique)
            connection.cls= self.clients
            connection.ids= self.ids
            connection.unique= unique
            print(unique)
            connection.start()
#             connection.send("ahoj") ##when socket is connected send send to client that it was created and append it to cls

            
            for i in self.clients:
#                 i.send(Message(self.clients, "clients")) ## sending new list of clients
                i.send(Message(self.ids, "clients"))
                
            
            
    
class Connection(threading.Thread):
    cls=None
    ids= None
    unique=None
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        
        
    def run(self):
        
        self.conn.send(pickle.dumps(Message(self.unique,"yourid")))
        while True:
            data = self.conn.recv(4096)
            print(type(data))
            if not data: break
            if not self.is_pickle_stream(data):
                
                from_client = data.decode()
                
            else:
                print(self.cls)
                data= pickle.loads(data)
                
                
                if data.message == "coords":
                    
                    
                    for i in self.cls:
#                         if i.conn != data.data[2]: # this code is a bit faulty since data is an id
                        if i.unique != data.data[2]:
                            print(data.data)
                            print(data)
                            i.send(Message(data.data, "receive"))
                elif data.message == "release":
                    for i in self.cls:
#                         if i.conn != data.data[0]: # this code is a bit faulty since data is an id
                        if i.unique != data.data[0]:
                            print(data.data)
                            print(data)
                            i.send(Message(data.data, "released"))
                
                            
                            
                ##mousbutton release message
                
            
    def send(self, message):
        if type(message) is str:
            self.conn.send(message.encode())
            

        else:
          
            self.conn.send(pickle.dumps(message))
#             self.conn.send(message.encode())
    
    def is_pickle_stream(self,stream):
        try:
            pickle.loads(stream)
            return True
        except UnpicklingError:
            return False
        


        
    
if __name__ =="__main__":
    server = Server()
    server.start()

        