import socket
import http
import subprocess
import Crypto

class SchadenClient(object):
    def __init__(self):
        self.Cryptor = CryptoProvider()
        self.Holder = ExHandler()
        self.Coordinator = Coordinator()
        self.ConnectionManager = ConnectionManager()
        self.GateFabric = GateFabric()
        self.Inner_Gate = Gate()

    def run(self):
        #TODO
        return 0

    def stop(self):
        #TODO
        return 0


class CryptoProvider(object):
    def __init__(self):
        #TODO
        return 0

class ExHandler(object):
    def __init__(self):
        return 0
        #TODO

class _ConnectionManager(object):
    def __init__(self):
        self.connection_list = []

class Gate(object):
    def __init__(self, port = 50600, error_handler=None):
        self.addr = ('127.0.0.1', port)
        self._host_conn = ''
        self._host_addr = ''
        self.data = bytes()

        self.gateway = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)
        self.gateway.bind(self.addr)

    def open(self):
        while True:
            self.gateway.listen(5)
    
            self._host_conn, self._host_addr = self.gateway.accept()

            #self.data = self._host_conn.recv(2048)
            #self.data = self.data.decode('ascii')
            #print(self.data)
        return 0



if __name__ == '__main__':

    Main = SchadenClient.run()

