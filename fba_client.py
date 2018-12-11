from __future__ import print_function

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import sys
import json

port = sys.argv[1]
a = [{"foo":"$10"},
    {"bar":"$30"},
    {"foo":"$20"},
    {"bar":"$20"},
    {"foo":"$30"}]


class MulticastPingClient(DatagramProtocol):

    def startProtocol(self):
        # Join the multicast address, so we can receive replies:
        self.transport.joinGroup("228.0.0.5")
        # Send to 228.0.0.5:9999 - all listeners on the multicast address
        # (including us) will receive this message.
        for i in range(len(a)):
            s=json.dumps(a[i]).encode('utf-8')
            self.transport.write(s, ("228.0.0.5", 3010))
        s1=json.dumps(a[1]).encode('utf-8')
        self.transport.write(s1, ("228.0.0.5", 3010))


    def datagramReceived(self, datagram, address):
        print("Datagram %s received from %s" % (repr(datagram), repr(address)))

def main():
    reactor.listenMulticast(int(port), MulticastPingClient(), listenMultiple=True)
    reactor.run()

if __name__ == '__main__':
    main()