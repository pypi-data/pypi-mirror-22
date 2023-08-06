#!/usr/bin/python

"""
dispynetrelay: Relay ping messages from client(s) to nodes
in a network; see accompanying 'dispy' for more details.
"""

import sys
import socket
import traceback
import struct
try:
    import netifaces
except:
    netifaces = None

import dispy
import asyncoro

__author__ = "Giridhar Pemmasani (pgiri@yahoo.com)"
__email__ = "pgiri@yahoo.com"
__copyright__ = "Copyright 2011, Giridhar Pemmasani"
__contributors__ = []
__maintainer__ = "Giridhar Pemmasani (pgiri@yahoo.com)"
__license__ = "MIT"
__url__ = "http://dispy.sourceforge.net"
__status__ = "Production"
__version__ = dispy._dispy_version
__all__ = []

logger = asyncoro.Logger('dispynetrelay')
from asyncoro import Coro, serialize, deserialize, AsyncSocket


class DispyNetRelay(object):
    """Internal use only.
    """

    def __init__(self, ip_addr=None, node_port=51348, listen_port=0,
                 scheduler_node=None, scheduler_port=51347):
        self.addrinfo = dispy.node_addrinfo(ip_addr)
        if not listen_port:
            listen_port = node_port
        self.node_port = node_port
        self.listen_port = listen_port
        self.scheduler_port = scheduler_port
        self.scheduler_ip_addrs = list(filter(lambda ip: bool(ip),
                                              [dispy._node_ipaddr(scheduler_node)]))
        self.listen_udp_coro = Coro(self.listen_udp_proc)
        self.listen_tcp_coro = Coro(self.listen_tcp_proc)
        self.sched_udp_coro = Coro(self.sched_udp_proc)
        if self.addrinfo.family == socket.AF_INET:
            self._broadcast = '<broadcast>'
            if netifaces:
                for iface in netifaces.interfaces():
                    for link in netifaces.ifaddresses(iface).get(netifaces.AF_INET, []):
                        if link['addr'] == self.addrinfo.ip:
                            self._broadcast = link.get('broadcast', '<broadcast>')
                            break
                    else:
                        continue
                    break
        else: # self.addrinfo.sock_family == socket.AF_INET6
            self._broadcast = 'ff05::1'
            self.mreq = socket.inet_pton(self.addrinfo.family, self._broadcast)
            self.mreq += struct.pack('@I', self.addrinfo.ifn)
        logger.info('version %s started', dispy._dispy_version)

    def listen_udp_proc(self, coro=None):
        coro.set_daemon()
        bc_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_DGRAM))
        if self.addrinfo.family == socket.AF_INET:
            bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else: # self.sock_family == socket.AF_INET6
            bc_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS,
                               struct.pack('@i', 1))
            bc_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, self.addrinfo.ifn)
        bc_sock.bind((self.addrinfo.ip, 0))
        if self.scheduler_ip_addrs and self.scheduler_port:
            relay_request = {'ip_addrs': self.scheduler_ip_addrs, 'port': self.scheduler_port,
                             'version': __version__, 'sign': None}
            bc_sock.sendto('PING:'.encode() + serialize(relay_request),
                           (self._broadcast, self.node_port))

        listen_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_DGRAM))
        if self.addrinfo.family == socket.AF_INET:
            listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else: # self.addrinfo.family == socket.AF_INET6
            listen_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, self.mreq)
        listen_sock.bind(('', self.listen_port))

        while 1:
            msg, addr = yield listen_sock.recvfrom(1024)
            if not msg.startswith('PING:'.encode()):
                logger.debug('Ignoring message "%s" from %s',
                             msg[:min(len(msg), 5)], addr[0])
                continue
            logger.debug('Ping message from %s (%s)', addr[0], addr[1])
            try:
                info = deserialize(msg[len('PING:'.encode()):])
                if info['version'] != __version__:
                    logger.warning('Ignoring %s due to version mismatch: %s / %s',
                                   info['ip_addrs'], info['version'], __version__)
                    continue
                self.scheduler_ip_addrs = info['ip_addrs'] + [addr[0]]
                self.scheduler_port = info['port']
            except:
                logger.debug('Ignoring ping message from %s (%s)', addr[0], addr[1])
                logger.debug(traceback.format_exc())
                continue
            if info.get('relay', None):
                logger.debug('Ignoring ping back (from %s)', addr[0])
                continue
            logger.debug('relaying ping from %s / %s', info['ip_addrs'], addr[0])
            if self.node_port == self.listen_port:
                info['relay'] = 'y'  # 'check if this message loops back to self

            yield bc_sock.sendto('PING:'.encode() + serialize(info), addr)

    def listen_tcp_proc(self, coro=None):
        coro.set_daemon()
        tcp_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_STREAM))
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind(('', self.listen_port))
        tcp_sock.listen(8)

        bc_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_DGRAM))
        if self.addrinfo.family == socket.AF_INET:
            bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else: # self.addrinfo.sock_family == socket.AF_INET6
            bc_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS,
                               struct.pack('@i', 1))
            bc_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, self.addrinfo.ifn)
        bc_sock.bind((self.addrinfo.ip, 0))
        auth_len = len(dispy.auth_code('', ''))

        def tcp_task(conn, addr, coro=None):
            conn.settimeout(5)
            try:
                msg = yield conn.recvall(auth_len)
                msg = yield conn.recv_msg()
            except:
                logger.debug(traceback.format_exc())
                logger.debug('Ignoring invalid TCP message from %s:%s', addr[0], addr[1])
                raise StopIteration
            finally:
                conn.close()
            logger.debug('Ping message from %s (%s)', addr[0], addr[1])
            try:
                info = deserialize(msg[len('PING:'.encode()):])
                if info['version'] != __version__:
                    logger.warning('Ignoring %s due to version mismatch: %s / %s',
                                   info['ip_addrs'], info['version'], __version__)
                    raise StopIteration
                # TODO: since dispynetrelay is not aware of computations
                # closing, if more than one client sends ping, nodes will
                # respond to different clients
                self.scheduler_ip_addrs = info['ip_addrs'] + [addr[0]]
                self.scheduler_port = info['port']
            except:
                logger.debug('Ignoring ping message from %s (%s)', addr[0], addr[1])
                logger.debug(traceback.format_exc())
                raise StopIteration
            if info.get('relay', None):
                logger.debug('Ignoring ping back (from %s)', addr[0])
                raise StopIteration
            logger.debug('relaying ping from %s / %s', info['ip_addrs'], addr[0])
            if self.node_port == self.listen_port:
                info['relay'] = 'y'  # 'check if this message loops back to self
            yield bc_sock.sendto('PING:'.encode() + serialize(info),
                                 (self._broadcast, self.node_port))

        while 1:
            conn, addr = yield tcp_sock.accept()
            Coro(tcp_task, conn, addr)

    def sched_udp_proc(self, coro=None):
        coro.set_daemon()
        sched_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_DGRAM))
        if self.addrinfo.family == socket.AF_INET:
            sched_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else: # self.addrinfo.family == socket.AF_INET6
            sched_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, self.mreq)

        sched_sock.bind(('', self.scheduler_port))

        while 1:
            msg, addr = yield sched_sock.recvfrom(1024)
            if (not msg.startswith('PING:'.encode()) or
               not self.scheduler_ip_addrs or not self.scheduler_port):
                logger.debug('Ignoring ping message from %s (%s)', addr[0], addr[1])
                continue
            try:
                info = deserialize(msg[len('PING:'.encode()):])
                assert info['version'] == __version__
                # assert isinstance(info['cpus'], int)
            except:
                logger.debug(traceback.format_exc())
            msg = {'ip_addrs': self.scheduler_ip_addrs, 'port': self.scheduler_port,
                   'version': __version__}
            if info.get('relay', None):
                logger.debug('Ignoring ping back from %s: %s', addr[0], info)
                continue
            msg['relay'] = 'y'
            relay_sock = AsyncSocket(socket.socket(self.addrinfo.family, socket.SOCK_DGRAM))
            relay_sock.bind((self.addrinfo.ip, 0))
            yield relay_sock.sendto('PING:'.encode() + serialize(msg),
                                    (info['ip_addr'], info['port']))
            relay_sock.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', dest='loglevel', default=False,
                        help='if given, debug messages are printed')
    parser.add_argument('-i', '--ip_addr', dest='ip_addr', default='',
                        help='IP address to use (may be needed in case of multiple interfaces)')
    parser.add_argument('--scheduler_node', dest='scheduler_node', default='',
                        help='name or IP address of scheduler to announce when starting')
    parser.add_argument('--scheduler_port', dest='scheduler_port', type=int, default=51347,
                        help='port number used by scheduler')
    parser.add_argument('--node_port', dest='node_port', type=int, default=51348,
                        help='port number used by nodes')
    parser.add_argument('--listen_port', dest='listen_port', type=int, default=0,
                        help='port number to listen (instead of node_port) '
                        'for connection from client')
    config = vars(parser.parse_args(sys.argv[1:]))
    # print(config)

    if config['loglevel']:
        logger.setLevel(logger.DEBUG)
    else:
        logger.setLevel(logger.INFO)
    del config['loglevel']

    DispyNetRelay(**config)

    while True:
        try:
            cmd = raw_input('Enter "quit" or "exit" to terminate dispynetrelay: ')
            cmd = cmd.strip().lower()
            if cmd == 'quit' or cmd == 'exit':
                break
        except KeyboardInterrupt:
            # TODO: terminate even if jobs are scheduled?
            logger.info('Interrupted; terminating')
            break
        except:
            logger.debug(traceback.format_exc())
