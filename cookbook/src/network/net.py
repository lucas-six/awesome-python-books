#!/usr/bin/env python

# Copyright (c) 2014-2015 Li Yun <leven.cn@gmail.com>
# All Rights Reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''TCP/IP Networking Extension

Including:

- TCP request (blocking/timeout mode, IPv4/IPv6)
- TCP server (blocking/timeout/non-blocking mode, IPv4, multi-threads)
- TCP Handler

@since Python 3.4
'''

import sys
from abc import ABCMeta, abstractmethod
import errno
import time
import socket
import threading
import selectors


def _eintr_retry(func, *args):
    '''Ignore the signal <code>EINTR</code>.

    @param func system call
    @param args arguments of system call
    @return results of system call
    @exception OSError raised by the system call
    '''

    while True:
        try:
            return func(*args)
        except OSError as err:
            if err.errno != errno.EINTR:
                raise


class TCPRequest(object):
    '''A TCP request over IPv4/IPv6.
    '''

    def __init__(self, addr, timeout=None, reconn_times=3, wait_time=0.3, increase_time=0.1,
            ipv4only=True):
        '''Create a TCP request over IPv4/IPv6.

        @param addr server address, 2-tuple of (host, port). An host of '' or port
                    0 tells the OS to use the default.
        @param timeout timeout of socket object. None for blocking, 0.0 for
                       non-blocking, others for timeout in seconds (float)
        @param reconn_times 重连次数
        @param wait_time 每次重连等待时间间隔（秒，浮点数）
        @param increase_time 每次重连后增加的等待时间间隔（秒，浮点数）
        @param ipv4only True for IPv4 only, False for both IPv6/IPv4.
        @return socket object
        @exception ValueError parameter error
        @exception OSError <code>socket</code> error

        @see getsockname()
        @see getpeername()
        @see recv_into()
        '''

        if timeout == 0.0:
            # BlockingIOError (WSAEWOULDBLOCK on Windows) would be raised
            raise ValueError('NOT support for non-blocking mode')

        self._reconn_times = reconn_times
        self._wait_time = wait_time
        self._increase_time = increase_time
        self._sock = None

        if ipv4only:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(timeout)
            self._connect(addr)
        else:  # both IPv6 and IPv4, prefer to IPv6
            host, port = addr
            err = None
            for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
                family, socktype, proto, canonname, sockaddr = res
                self._sock = None
                try:
                    self._sock = socket(family, socktype, proto)
                    self._sock.settimeout(timeout)
                    self._connect(sockaddr)
                except OSError as _:
                    err = _

            if err is not None:
                raise err
            else:
                raise OSError("getaddrinfo returns an empty list")

    def close(self):
        '''Close the requst.
        '''
        if __debug__:
            print('{} closed'.format(self._sock.getsockname()), file=sys.stderr)
        self._sock.close()

    def send(self, data):
        '''Send data to server.

        @exception OSError <code>socket</code> error
        '''
        self._sock.sendall(data)

    def recv(self, nbytes):
        '''Receive data from server.

        @param nbytes up to <code>nbytes</code> bytes to received
        @return a bytes object representing the data received
        @exception OSError <code>socket</code> error

        For best match with hardware and network realities, the value of
        <code>nbytes</code> should be a relatively small power of 2, for
        example, <value>4096</value>.
        '''
        return self._sock.recv(nbytes)

    def _connect(self, addr):
        '''连接服务器.

        @param addr server address, 2-tuple of (host, port). An host of '' or port
                    0 tells the OS to use the default.
        @exception OSError <code>socket</code> error
        '''
        while True:
            try:
                _eintr_retry(self._sock.connect, addr)
            except OSError as err:
                # When a timeout occurs on a socket which has had timeouts
                # enabled via a prior call to <code>settimeout()</code>,
                # <code>socket.timeout</code> would be raised, instead of
                # <code>errno.ETIMEDOUT</code>
                # Li Yun <leven.cn@gmail.com>: This should be an issue.
                if err.errno == errno.ECONNREFUSED or isinstance(err, socket.timeout):
                    # Try to reconnect
                    reconn_times = self._reconn_times
                    wait_time = self._wait_time
                    if reconn_times > 0:
                        reconn_times -= 1
                        time.sleep(wait_time)
                        wait_time += self._increase_time
                        if __debug__:
                            print('Reconnect...', file=sys.stderr)
                        continue
                    else:
                        raise

                # already connected
                elif err.errno == errno.EISCONN:
                    break

                # other errors
                else:
                    raise


class BaseRequestHandler(object):
    '''Base class for request handler classes.

    This class is instantiated for each request to be handled.  The
    constructor sets the instance variables request, client_address
    and server, and then calls the handle() method.  To implement a
    specific service, all you need to do is to derive a class which
    defines a handle() method.

    The handle() method can find the request as self.request, the
    client address as self.client_address, and the server (in case it
    needs access to per-server information) as self.server.  Since a
    separate instance is created for each request, the handle() method
    can define arbitrary other instance variariables.
    '''

    __meta__ = ABCMeta

    def __init__(self, request, server):
        self.request = request
        self.client_address = self.request.getsockname()
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    @abstractmethod
    def handle(self):
        pass

    def finish(self):
        pass


class TCPRequestHandler(BaseRequestHandler):
    '''TCP request handler.
    '''

    # 客户端默认为阻塞模式
    timeout = None

    # Disable nagle algorithm for this socket, if True.
    # Use only when wbufsize != 0, to avoid small packets.
    disable_nagle_algorithm = False

    def setup(self):
        self.request.settimeout(self.timeout)
        if self.disable_nagle_algorithm:
            self.request.setsockopt(socket.IPPROTO_TCP,
                                       socket.TCP_NODELAY, True)

    def finish(self):
        if self.server.timeout == 0.0:
            self.server.sel.unregister(self.request)
        try:
            #explicitly shutdown.  socket.close() merely releases
            #the socket and waits for GC to perform the actual close.
            self.request.shutdown(socket.SHUT_WR)
        except OSError:
            pass #some platforms may raise ENOTCONN here
        self.request.close()


class TCPServer(object):
    '''TCP Server (Only supported for IPv4).
    '''

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5  # used by <code>listen()</code>

    def __init__(self, address, request_handler=TCPRequestHandler,
            timeout=None, ipv4only=True):
        '''Create an instance of TCP server.

        @param address server address, 2-tuple (host, port)
        @param request_handler request handler class
        @param timeout timeout of socket object. None for blocking, 0.0 for
                       non-blocking, others for timeout in seconds (float)
        @param ipv4only True for IPv4 only, False for both IPv6/IPv4.
        @exception OSError <code>socket</code> error
        '''
        self.timeout = timeout
        self._RequestHandler = request_handler
        self._thread_pool = []

        # Setup
        self._sock = socket.socket(self.address_family, self.socket_type)
        self._sock.settimeout(self.timeout)

        # Bind
        if __debug__:
            # Re-use binding address for debugging purpose
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(address)
        self.server_address = self._sock.getsockname()

        # Active
        self._sock.listen(self.request_queue_size)

        # In non-blocking mode, I/O multiplex used
        if timeout == 0.0:
            # on Windows: select()
            # on Linux 2.5.44+: epoll()
            # on most UNIX system: poll()
            # on BSD (Including OS X): kqueue()
            #
            # @see select
            self.sel = selectors.DefaultSelector()
            self.sel.register(self._sock, selectors.EVENT_READ, self._handle_requests)

    def run(self, timeout=None):
        '''Run the server.

        @param timeout timeout for I/O multiplex
        @exception OSError <code>socket</code> error
        '''
        # Note: put the <code>while</code> loop inside the <code>except</code>
        # clause of a <code>try-except</code> statement and monitor for
        # <code>EOFError</code> or <code>KeyboardInterrupt</code> exceptions
        # so that you can close the server's socket in the
        # <code>except</code> or <code>finally</code> clauses.
        try:
            while True:
                if __debug__:
                    print('Waiting for request on port {0}...'
                        .format(self.server_address[1]), file=sys.stderr)

                if self.timeout == 0.0:
                    events = self.sel.select()
                    for key, mask in events:
                        callback = key.data
                        callback(key.fileobj, mask)

                # Blocking mode or timeout mode
                else:
                    self._handle_requests()

                if __debug__:
                    print('\n', file=sys.stderr)
        finally:
            self.close()

    def _handle_requests(self, server_sock=None, mask=None):
        '''Handle requests.

        @exception OSError <code>socket</code> error
        '''
        # <code>socket.accept()</code> cannot be interrupted by the signal
        # EINTR or <code>KeyboardInterrupt</code> in blocking mode on Windows.
        request, addr = self._sock.accept()
        print('Request from {0}'.format(addr))

        # Blocking mode
        if self.timeout is None:
            self._handle_one_request(request)

        # Non-blocking mode
        elif self.timeout == 0.0:
            request.settimeout(0.0)
            self.sel.register(request, selectors.EVENT_READ, self._handle_one_request)

        # timeout mode, handing each request in a thread
        else:
            request.settimeout(None)
            request_thread = threading.Thread(target=self._handle_one_request,
                    args=(request, ))
            self._thread_pool.append(request_thread)
            request_thread.start()

    def _handle_one_request(self, request, mask=None):
        '''Handle single one request.

        @param request request connection (socket object) from client
        @exception OSError <code>socket</code> error
        '''
        self._RequestHandler(request, self)

    def close(self):
        '''Close the server.
        '''
        for t in self._thread_pool:
            t.join()
        self._sock.close()
