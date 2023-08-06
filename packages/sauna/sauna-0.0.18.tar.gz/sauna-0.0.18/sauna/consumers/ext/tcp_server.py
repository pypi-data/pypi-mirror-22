import socket
import select
from collections import defaultdict

from sauna.consumers.base import AsyncConsumer
from sauna.consumers import ConsumerRegister

my_consumer = ConsumerRegister('TCPServer')


@my_consumer.consumer()
class TCPServerConsumer(AsyncConsumer):

    service_checks = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = {
            'port': config.get('port', 5555),
            'backlog': config.get('port', 128),
            'keepalive': config.get('keepalive', True)
        }
        self.read_wanted, self.write_wanted = ([], [])
        self.write_buffers = defaultdict(bytes)

    def _create_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', self.config['port']))
        self.server.listen(self.config['backlog'])

    def _accept_new_connection(self):
        client_socket, address = self.server.accept()
        self.logger.debug('New connection from {}'.format(address[0]))
        self.write_wanted.append(client_socket)
        self.read_wanted.append(client_socket)
        return client_socket

    def _activate_keepalive(self, s, after_idle_sec=30, interval_sec=10,
                            max_fails=5):
        """Set TCP keepalive on an open socket.

        It activates after 30 second (after_idle_sec) of idleness,
        then sends a keepalive ping once every 10 seconds (interval_sec),
        and closes the connection after 5 failed ping (max_fails).
        """
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

    def _close_socket(self, s):
        try:
            s.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        try:
            s.close()
        except socket.error:
            pass
        self._remove_from_list(self.write_wanted, s)
        self._remove_from_list(self.read_wanted, s)
        try:
            del self.write_buffers[s]
        except KeyError:
            pass
        self.logger.debug('Closed connection')

    @staticmethod
    def _remove_from_list(list_, value):
        while value in list_:
            try:
                list_.remove(value)
            except ValueError:
                pass

    def _handle_read_event(self, s):
        if s == self.server:
            client_socket = self._accept_new_connection()
            if self.config['keepalive']:
                self._activate_keepalive(client_socket)
            to_write = self.get_current_status()[0].encode() + b'\n'
            self.write_buffers[client_socket] += to_write
            self.write_wanted.append(client_socket)
        else:
            try:
                read_data = s.recv(4096)
            except socket.error as e:
                self.logger.debug(
                    'Error while receiving, closing connection: {}'.format(e)
                )
                self._close_socket(s)
                return
            if len(read_data) == 0:
                self._close_socket(s)
            else:
                self.logger.debug('Received data')
                if b'\n' in read_data:
                    to_write = self.get_current_status()[0].encode() + b'\n'
                    self.write_buffers[s] += to_write
                    self.write_wanted.append(s)

    def _handle_write_event(self, s):
        try:
            sent_len = s.send(self.write_buffers[s])
        except socket.error as e:
            self.logger.debug(
                'Error while sending, closing connection: {}'.format(e)
            )
            self._close_socket(s)
            return
        self.write_buffers[s] = self.write_buffers[s][sent_len:]
        if not self.write_buffers[s]:
            self.write_wanted.remove(s)
            self.logger.debug('Sent data')

    def run(self, must_stop, *args):
        self._create_server()
        self.read_wanted = [self.server]
        self.write_wanted = []

        while not must_stop.is_set():
            readable, writable, errored = select.select(
                self.read_wanted,
                self.write_wanted,
                self.read_wanted + self.write_wanted,
                1
            )

            for s in errored:
                self.logger.debug('Connection in error, closing it')
                self._close_socket(s)

            for s in readable:
                self._handle_read_event(s)

            for s in writable:
                self._handle_write_event(s)

        self.logger.debug('Exited consumer thread')

    @staticmethod
    def config_sample():
        return '''
        # Listen on a TCP port and serve results to incoming connections
        - type: TCPServer
          port: 5555
        '''
