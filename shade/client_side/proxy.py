'''
Shade client is a simle local proxy which is used to process the clients
traffic through the layer of different middlewares - modules designed to
modificate the packages in a special way (encryption, first of all). 
'''

import socket
import http
import subprocess
import Crypto


class ShadeClient(object):
    '''Main clients object, manages all the other operations. Should be the SINGLE
    instance of this class in the application'''
    def __init__(self):
        self.holder = ExHandler()
        self.coordinator = Coordinator()
        self.connection_manager = ConnectionManager()
        self.inner_gate = InnerGate()

    def run(self):
        '''Launchs the application, starts the main loop'''
        self.inner_gate.open()

        while True:

        return 0

    def stop(self):
        '''Correctly stops the application, should be use in whatever conditions,
        even if an error has been occured. Should be called by EventHandler in
        critical cases.'''
        #TODO
        return 0


class MODULE_CryptoProvider(object):
    '''Middleware module used to encrypt the users traffic'''
    def __init__(self):
        #TODO
        return 0


class EvHandler(object):
    '''Should be the single instance of this class per application. EventHadler is used
    for logging and solving the exceptional situations if it is possible. Debug
    is also the reason to use EvHandler'''
    def __init__(self):
        return 0
        #TODO


class ConnectionManager(object):
    '''ConnectionManager watchs over the connections tunnels - links between the
    connections (sockets) established by the InnerGate and ExternalGates. It is 
    responsible for managing the taffics retransmission to the MiddlewareManager.
    IMPORTANT NOTE: Don`t use the ConnectionManager to directly pass the data to the
    middleware modules. Use the MiddlewareManager instead'''
    def __init__(self):
        self.connection_table = {}
        self.condescriptor = 0

    def register(self, reqconn, reqaddr):
        self.connection_table[self._get_descriptor()] = (reqconn, reqaddr)
        self.recv_msg()

    def _get_descriptor(self):
        self.conndescriptor += 1
        return self.conndescriptor

class MiddlewareManager(object):
    '''MiddlewareManager is used to manage the data passing through the middleware layer'''
    def __init__(self):
        pass


class Gate(object):
    '''Prototype class for Inner and External classes. It is also can be used as
    the wrapper over the any other connection socket, but it is strongly reccomended
    to use it as an abstract one'''
    def __init__(self, event_handler=None):
        self.error = event_handler
        self.gateway = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)

        self.closemark = False

    def open(self):
        '''Abstract method, prototype for the methods used to start the gates main
        functional. Throws a warning if the gate is closed.'''
        if self.closemark:
            event_handler.warn('gate_closed', 3)
            return -1
            
        self.gateway.bind(self.addr)

    def close(self):
        '''Abstract method (but is universal enough to be used in most cases) to end
        the life of the gate and close all the connections established in it at the moment.
        NOTE: it is impossible to use the closed Gate anymore. Closed gates should be garbagecollected,
        close() method is designed to prepare gates to it'''
        self.gateway.shutdown(socket.SHUT_RDWR)
        self.gateway.close()
        self.closemark = True


class InnerGate(Gate):
    '''InnerGate is the main proxy socket wrapper, which is used as the representative of the 
    proxy system to to the clients application - something that generates the traffic. InnerGate
    is responsible for establishing connections between the client and the clients proxy-script
    and then send it to the ConnectionManager.
    NOTE: Don`t use InnerGate to send responses for the clients requests. It is the task for 
    ConnectionManager'''
    def __init__(self, port = 50600, event_handler=None):
        super().__init__(event_handler)
        self.received_conn = ''
        self.received_addr = ''
        self.addr = ('127.0.0.1', port)

    def open(self, conmanager):
        super().open()

        while True:
            self.gateway.listen(5)
    
            self.received_conn, self.received_addr = self.gateway.accept()
            conmanager.register(self.received_conn, self.received_addr)

    def close(self):
        super().close()


class ExternalGate(Gate):
    '''ExternalGates are used to communicate with the remote ShadeServer, which will commutate the clients
    cleared traffic'''
    def __init__(self, shadeserv, event_handler=None):
        super().__init__(event_handler)
        self.gateway.connect(shadeserv)

    def close(self):
        super().__init__(event_handler)


if __name__ == '__main__':
    Main = ShadeClient.run()

