from __future__ import print_function

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import sys
import json
import pickle

all_server_ports = [3010, 3011, 3012, 3013]
port = sys.argv[1]
send_port = [3010, 3011, 3012, 3013]
send_port.remove(int(port))
vote_broadcast = ""
file_name = "testfile" + sys.argv[1]
print(file_name)
fileObject = open(file_name,'wb') 

vote_count = []


class MulticastPingPong(DatagramProtocol):


    def startProtocol(self):
        self.broadcast = 0
        self.message_len = 0 
        self.vote_state = []  
        self.accept_state = [] 
        self.vote_count = 1  
        self.accept_count = 1
        self.state = 0
        self.message = []
        self.file_Name = []
        """
        Called after protocol has started listening.
        """
         # Set the TTL>1 so multicast will cross router hops:
        self.transport.setTTL(5)
         # Join a specific multicast group:
        self.transport.joinGroup("228.0.0.5")
        

    def datagramReceived(self, datagram, address):
        port_received_from = repr(address)
        print("Datagram %s received from %s" % (repr(datagram), repr(address)))
            # Rather than replying to the group multicast address, we send the
            # reply directly (unicast) to the originating port:
       

        if self.broadcast == 0 or self.message_len < 6:  
            #self.message.append(datagram)
            #fileObject = open(self.file_Name,'wb')
            #pickle.dump(self.message,fileObject)
            #fileObject.close()
            self.broadcast_all(datagram,address)
            self.message_len = self.message_len + 1
            
        self.broadcast = 1
        

        


    
        # for each in send_port:
        #         self.transport.write(datagram, ("228.0.0.5", int(each)))
        #         data_address = str(datagram) + "," + port
        #         print(data_address)
        #     ##print(vote_state)
        #         vote_state.append(each)
        # if len(vote_state) >= 3:
        #     for each in send_port:
        #         self.transport.write(b"vote", ("228.0.0.5", int(each)))

    def broadcast_all(self,datagram,address):
       for i in range(len(send_port)):
           self.transport.write(datagram, ("228.0.0.5", send_port[i]))
           self.message.append(datagram)
           pickle.dump(self.message,fileObject) 
           self.vote_count = self.vote_count + 1
       if self.vote_count > 2:
           print("Datagram vote received from %s" % (send_port))
       if self.accept_count > 2:
           print("Datagram %s" %(repr(datagram)))
           print("Datagram accepted from %s" % (send_port))
           print("vote confirmed from %s" % (send_port))


       
        
           
    def vote(self,datagram):
        for i in range(len(send_port)):
            if self.vote_count > 2:
                datagram1 = datagram + b"vote"
                #self.transport.write(datagram1, ("228.0.0.5", send_port[i]))
                self.vote_count = self.vote_count + 1
                if self.vote_count > 2:
                    print("Datagram vote received from %s" % (send_port))
                self.accept_count = 3
                if self.accept_count > 2:
                    print("Datagram %s" %(repr(datagram)))
                    print("Datagram accepted from %s" % (send_port))
                    print("vote confirmed from %s" % (send_port))


            

            

    
                
            
            

        

    # def vote(self):
    #     if len(vote_count) > 2:
    #         for i in range(len(send_port)):
    #             self.transport.write(b"vote", ("228.0.0.5", send_port[i]))
            # if send_port[i] == 3010:
            #     self.vote_count = self.vote_count+1
            #     print(self.vote_count)
            #     if self.vote_count == 2:
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[2]))
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[1]))
            
            # if send_port[i] == 3011:
            #     self.vote_count = self.vote_count+1
            #     print(self.vote_count)
            #     if self.vote_count == 2:
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[0]))
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[1]))
            
            # if send_port[i] == 3012:
            #     self.vote_count = self.vote_count+1
            #     print(self.vote_count)
            #     if self.vote_count == 2:
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[0]))
            #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[2]))
                    
            
        
        # for i in range(len(send_port)):
        #     if self.vote_count > 2:
        #         self.transport.write(datagram + b"vote", ("228.0.0.5", send_port[i]))
        # self.vote_count = 1
                        
                #self.accept_state = self.accept_state + 1

    #     if self.vote_count > 2:
    #         print(message)
    #         datagram = datagram + b"vote"
    #         self.broadcast_all(datagram)




        


        

           # vote_broadcast = data_address + "," + "vote"
           # print(vote_broadcast)
           # bytes1 = bytes(vote_broadcast, 'utf-8')
           # for each in send_port:             
  
# We use listenMultiple=True so that we can run MulticastServer.py and
# MulticastClient.py on same machine:
reactor.listenMulticast(int(port), MulticastPingPong(), listenMultiple=True)

reactor.run()