import socket
import http
import subprocess
import Crypto

class SchadenClient(object):
    def __init__(self):
        self.cryptor = CryptoProvider()
        self.holder = ExHandler()
        self.coordinator = Coordinator()
        self.connection_manager = ConnectionManager()
        self.inner_gate = Gate()

    def run(self):
        self.inner_gate.open()

        while True:

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
    def __init__(self, error_handler=None):
        self.error = error_handler

    def open(self):
        self.gateway.bind(self.addr)
        while True:
            self.gateway.listen(5)
    
            self._host_conn, self._host_addr = self.gateway.accept()
            self.data = self._host_conn.recv(2048)
            self.data = self.data.decode('ascii')

        return 0

class InnerGate(Gate):
    def __init__(self, port = 50600, error_handler=None):
        super().__init__(error_handler)
        self.received_conn = ''
        self.received_addr = ''
        self.addr = ('127.0.0.1', port)
        self.data = bytes()

        self.gateway = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)


if __name__ == '__main__':
    T_input = Gate()
    T_input.open()
    Main = SchadenClient.run()

