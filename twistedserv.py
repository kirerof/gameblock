from twisted.internet import reactor
from twisted.internet.protocol import Protocol, connectionDone
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint


class Server(Protocol):
    def __init__(self, users):
        self.users = users
        self.name = ''
        self.username = ''
        print(self, self.name)

    def connectionMade(self):
        print('New connection')

    def add_user(self, name):
        if name not in self.users:
            self.users[self] = name
            self.name = name
        else:
            self.transport.write('wrong username, try another'.encode('utf-8'))

    turn = 1

    def dataReceived(self, data):
        data = data.decode('utf-8')
        username_list = ["kkkk", "kerich"]

        if not self.name:
            self.add_user(data)
            # return

        for protocol in self.users.keys():
            if protocol != self and data not in username_list:
                print("коорд ", self.username, data)
                protocol.transport.write(f'{data}'.encode('utf-8'))
            if protocol == self and data in username_list:
                self.username = data
                if Server.turn % 2:
                    protocol.transport.write('x'.encode('utf-8'))
                else:
                    protocol.transport.write('0'.encode('utf-8'))
                Server.turn += 1

    def connectionLost(self, reason=connectionDone):
        del self.users[self]


class ServerFactory(ServFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Server(self.users)


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 6060)
    endpoint.listen(ServerFactory())
    reactor.run()
