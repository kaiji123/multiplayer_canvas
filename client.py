import pygame
import socket
import time
import threading
import pickle
from message import Message
class Game:
    client = None
    def __init__(self):
        pygame.init()
        c = Client()
        c.start()
        
        self.screen =pygame.display.set_mode((800,600),pygame.RESIZABLE )
        flip = pygame.display.flip
        getevents = pygame.event.get
        
        self.old_x =None
        self.old_y = None
        
        while True:
            if c.players != None:
#                 print("drawing for player")
                for i in c.players:
                    
                    if i.changed == True:
                        
                        print("DRAWING")
                        
                        pygame.draw.line(self.screen,(0,0,255),(i.old_x, i.old_y), (i.new_x, i.new_y ))
                        i.old_x = i.new_x
                        i.old_y= i.new_y
                        i.changed = False
                        print(i.identity)
                        
                
                
            for e in getevents():
                if e.type == pygame.VIDEORESIZE:
                    pass
                elif e.type == pygame.QUIT:
                    pygame.quit()
                    
                elif e.type == pygame.KEYDOWN:
                    print('KEYDOWN-' + e.unicode)
                elif pygame.mouse.get_pressed()[0]:
                    print("hel")

                    mx, my = pygame.mouse.get_pos()
                    if self.old_x ==None:
                        
                        self.old_x = mx
                        self.old_y = my
                    else:
                        color = (255,0,0)
                        pygame.draw.line(self.screen,color,(self.old_x, self.old_y), (mx, my ))
                        self.old_x=mx
                        self.old_y= my
                    xy = Message([mx,my, c.unique],"coords")
                    print(xy.message)
                    c.sendserver(pickle.dumps(xy))
                    
                elif e.type == pygame.MOUSEBUTTONUP:
                    self.old_x = None
                    self.old_y =None
#                     experimenting
                    print(c.players[c.checkid(c.players,c.unique)])
                    xy = Message([ c.unique],"release")
                    c.sendserver(pickle.dumps(xy))
                    

            flip()
# s= Game()

class Client(threading.Thread):
    client=None
    players=None #number of players
    data= None
    changed = False
    changedindex=None
    unique= None
    
    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 8080))
        while True:
            data = self.client.recv(4096)
            if not self.is_pickle_stream(data):
                from_server = data.decode()
                if from_server =="ahoj":
                    print("ahoj received")
                
            else:
                data= pickle.loads(data)
                self.data= data
                
                print(data)
                if data.message== "receive":
#                     if self.check(players,data[2]) != False:
#                         arr[self.check(players,data[2])].
                    
                    self.changed =True
                    print("socket changed")
                    self.changedindex = self.checkid(self.players,data.data[2])
                    print(self.players)
                    print(self.changedindex)
                    print("old",self.players[self.changedindex].old_x )
                    if self.players[self.changedindex].old_x == None:
                        print("assigning old", data.data)
                        
                        self.players[self.changedindex].old_x = data.data[0]
                   
                        self.players[self.changedindex].old_y= data.data[1]
                    else:
                        self.players[self.changedindex].new_x =data.data[0]
                        self.players[self.changedindex].new_y= data.data[1]
                        self.players[self.changedindex].changed =True
                        print("player changed")
                elif data.message=="released":
#                      self.changed =True
                    print("socket changed")
                    self.changedindex = self.checkid(self.players,data.data[0])
                    print(self.players)
                    print(self.changedindex)
                    print("old",self.players[self.changedindex].old_x )
                    self.players[self.changedindex].old_x =None
                    self.players[self.changedindex].old_y =None
                    self.players[self.changedindex].new_x =None
                    self.players[self.changedindex].new_y =None
                    self.players[self.changedindex].changed =False
                    
                    
#                     self.players[changedindex]
                elif data.message== "clients":
                    if self.players == None:
#                         self.players= data.data
                        
                        
                        self.players = [Player(i) for i in data.data] # assigning players
                        
                
                    else:
                        for i in data.data:
#                             if not self.checkplayer(self.players,i):
#                                 self.players.append(Player(i))
                            if not self.checkplayerid(self.players,i):
                                self.players.append(Player(i))
                elif data.message == "yourid":
                    self.unique = data.data
                    

                            
                                
                            
                
                        
        
                
            
            print(type(data))
            
           
                
            
            
    def sendserver(self, message):
        self.client.send(message)
        
    def check(self, arr, conn):#perform a check
        if arr == None:
            return False
        for i in arr:
            if i.connection == conn:
                return arr.index(i)
        return False
    def checkplayer(self, players, connection):
        for i in players:
            if i.connection == connection.conn:
                return True
        return False
    
    def checkid(self, arr, uniqueid):#perform a check
        if arr == None:
            return False
        for i in arr:
            if i.identity == uniqueid:
                return arr.index(i)
        return False
    def checkplayerid(self, players, ide):
        for i in players:
            if i.identity == ide:
                return True
        return False
    def is_pickle_stream(self, data):
        try:
            s=pickle.loads(data)
            return True
        except:
            return False
    
        
        
        
class Player:
    old_x= None
    old_y=None
    new_x= None
    new_y= None
#     connection= None
    changed = False # this determines if the coordinate is changed or not
    identity= None
#     def __init__(self, connection):
#         self.connection= connection
    def __init__(self, identity):
        self.identity= identity
        
        
        
s= Game()

        
    
        