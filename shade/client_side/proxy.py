'''
Shade client is a simle local proxy which is used to process the clients
traffic through the layer of different middlewares - modules designed to
modificate the packages in a special way (encryption, first of all). 
'''

import socket
import threading
import configparser
import queue
import time


class ShadeClient(object):
    '''Main clients object, manages all the other operations. Should be the SINGLE
    instance of this class in the application'''

    def __init__(self):
        self.configuration = { #DEBUG CONSTANTS SHOULD BE REMOVED IN PRODUCTION
            'TunnelsCount' : 6,
            'MaxConnPerTunnel' : 50,
            'Middlewares' : ['middle1.py', 'middle2.py'],
        }
        self.config()

        self.holder = EvHandler(self.configuration)
        self.connection_manager = ConnectionManager(self.configuration)
        self.inner_gate = InnerGate(self.configuration)

    def run(self):
        '''Launchs the application, starts the main loop'''

        self.inner_gate.open()

        while True:
            pass

        return 0

    def stop(self):
        '''Correctly stops the application, should be use in whatever conditions,
        even if an error has been occured. Should be called by EventHandler in
        critical cases.'''

        #TODO
        return 0

    def config(self):

        conf = configparser.ConfigParser()
        #TODO


class EvHandler(object):
    '''Should be the single instance of this class per application. EventHadler is used
    for logging and solving the exceptional situations if it is possible. Debug
    is also the reason to use EvHandler'''

    def __init__(self):
        return 0
        #TODO

    def warn(self):
        pass
        #TODO


class Tunnel(object):
    '''doc'''

    def __init__(self, qMax, cmanager):
        self.stream = threading.Thread(target=self.run)
        self.queue = queue.Queue(maxsize=qMax)
        self.qu_congestion = 0
        self.qu_limit = qMax
        self.middleware_processor = MiddlewareManager()
        self.conmanager = cmanager
        self.gate = ExternalGate()

    def run(self):
        while True:
            if self.queue.empty:
                time.sleep(0.3)
                continue

            proceed_data = self.middleware_processor.prepare(self.queue.get())
            response = self.gate.send(proceed_data)
            
            responsed_data = self.middleware_processor.retrieve(response)
            self.conmanager.return_to_client(retrieved_data, descriptor)
            self.qu_congestion = self.qu_congestion - 1

    def get_capacity(self):
        return qu_limit - qu_congestion

    def enqueue(self, _data, _descriptor):
        self.queue.put((_data, _descriptor))


class ConnectionManager(object):
    '''ConnectionManager watchs over the connections tunnels - links between the
    connections (sockets) established by the InnerGate and ExternalGates. It is 
    responsible for managing the taffics retransmission to the MiddlewareManager.
    IMPORTANT NOTE: Don`t use the ConnectionManager to directly pass the data to the
    middleware modules. Use the MiddlewareManager instead'''

    def __init__(self, conf, evhandler):
        self.handler = evhandler
        self.conf = conf
        self.connection_table = {}
        self.tunnels = []
        self.condescriptor = 0

        for i in range(self.conf[TunnelsCount]):
            self.tunnels.append(Tunnel(self.conf['MaxConnPerTunnel'], self))

    def register(self, reqconn, reqaddr):
        cur_desc = self._get_descriptor()
        self.connection_table[cur_desc] = (reqconn, reqaddr)
        data = self.recv_msg(reqconn)
        
        free_tunnel = self._get_able_tunnel()
        if free_tunnel:
            self.tunnels[free_tunnel].queue.put(data, cur_desc)
        else:
            self.handler.warn('tunnels_busy', 1)
            time.sleep(0.1)

    def recv_msg(self, conn):
        package = conn.recvmsg(1024)
        while True:
            data = conn.recvmsg(1024)
            if not data:
                break
            else:
                package+=data
        return package

    def return_to_client(self, data):
        pass
        #TODO

    def _get_able_tunnel(self):
        _free_tunnel = False
        _maximal = 0

        for _tunnel in enumerate(self.tunnels):
            _capacity = _tunnel[1].get_capacity()
            if _capacity > _maximal:
                _maximal = _capacity
                _free_tunnel = _tunnel[0]

        return _free_tunnel

    def _get_descriptor(self):
        self.conndescriptor += 1
        return self.conndescriptor

class MiddlewareManager(object):
    '''MiddlewareManager is used to manage the data passing through the middleware layer'''

    def __init__(self, configuration):
        
        self.config = configuration
        self.middleware_list = list(map((lambda x: 'middlewares/'+x), self.config['Middlewares']))
        self.middlewares = map(__import__, self.middleware_list)

    def prepare(self, data):
        '''Main method used to collaborate with middlewarers. Filters data through the layer
        of middleware. The middleware API is documented better in MIDDLEWARE.documentation (TODO).
        Main points: each middleware module should be represented as a .py script in the 
        "middleware" module and provide the "process" method, which takes the data argument - 
        the package, procceeded by the previous middleware (or the raw package, if it is the
        first) and returns the proceed data'''
        _data = data
        #TODO: Should exist the way to proceed data if there are no available middlewares enabled in config
        for mid in self.middlewares: 
            _data = mid.process(data) #NOTE: It is unclear, how should it work

        return _data

    def load(self, data):
        pass
        #TODO


class Gate(object):
    '''Prototype class for Inner and External classes. It is also can be used as
    the wrapper over the any other connection socket, but it is strongly reccomended
    to use it as an abstract one'''

    def __init__(self, event_handler=None):
        self.handler = event_handler
        self.gateway = socket.socket(family=socket.AF_INET,
                                     type=socket.SOCK_STREAM)

        self.closemark = False

    def open(self):
        '''Abstract method, prototype for the methods used to start the gates main
        functional. Throws a warning if the gate is closed.'''

        if self.closemark:
            self.handler.warn('gate_closed', 3)
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

    def send(self, data):
        self.gateway.sendall(data)
        response = bytes()
        while not reponse:
            response = self._recv_response(response)
            if response:
                break
            else:
                time.sleep(0.2)

        return response

    def _recv_response(self, resp):
        buffer = self.gateway.recv(2048)
        if buffer:
            return self._recv_response(resp+buffer)
        else:
            return resp


if __name__ == '__main__':
    Main = ShadeClient.run()

