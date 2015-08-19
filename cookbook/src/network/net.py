#!/usr/bin/env python3

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
- TCP request handler
- UDP request (IPv4)
- UDP server

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

        @param addr server address, 2-tuple of (host, port).
        @param timeout timeout of socket object. None for blocking, 0.0 for
                       non-blocking, others for timeout in seconds (float)
        @param reconn_times 重连次数
        @param wait_time 每次重连等待时间间隔（秒，浮点数）
        @param increase_time 每次重连后增加的等待时间间隔（秒，浮点数）
        @param ipv4only True for IPv4 only, False for both IPv6/IPv4.
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
        reconn_times = self._reconn_times
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


class BaseRequestHandler(metaclass=ABCMeta):
    '''Base class for request handler classes.

    This class is instantiated for each request to be handled.  The
    constructor sets the instance variables request, client_address and
    server, and then calls the handle() method.  To implement a specific
    service, all you need to do is to derive a class which defines a handle()
    method.

    The handle() method can find the request as self.request, and the server
    (in case it needs access to per-server information) as self.server.  Since
    a separate instance is created for each request, the handle() method can
    define arbitrary other instance variariables.
    '''

    # 客户端默认为阻塞模式
    timeout = None

    def __init__(self, request, server):
        self.request = request
        self.server = server
        self.request.settimeout(self.timeout)
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

    @see sendall()
    @see recv()
    '''

    # Disable nagle algorithm for this socket, if True.
    # Use only when wbufsize != 0, to avoid small packets.
    disable_nagle_algorithm = False

    def setup(self):
        if self.disable_nagle_algorithm:
            self.request.setsockopt(socket.IPPROTO_TCP,
                                       socket.TCP_NODELAY, True)

    def handle(self):
        pass

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
    '''TCP server (Only supported for IPv4).
   '''

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    # 启动TCP KeepAlive
    enable_keep_alive = False

    # 空闲时，启动探测间隔时间（秒）
    # Linux默认值为7200
    #     sysctl net.ipv4.tcp_keepalive_time
    # or
    #     cat /proc/sys/net/ipv4/tcp_keepalive_time
    # You can change the value to N.
    #      sudo sysctl -w net.ipv4.tcp_keepalive_time=<N>
    # or make the change permanently in "/etc/sysctl.conf".
    keep_alive_time = 1800

    # 网络不可达时，重发探测间隔时间（秒）
    # Linux默认值为75
    #     sysctl net.ipv4.tcp_keepalive_intvl
    # or
    #     cat /proc/sys/net/ipv4/tcp_keepalive_intvl
    # You can change the value to N.
    #      sudo sysctl -w net.ipv4.tcp_keepalive_intvl=<N>
    # or make the change permanently in "/etc/sysctl.conf".
    keep_alive_intvl = 1

    # 网络不可达时，重发探测次数
    # Linux默认值为9
    #     sysctl net.ipv4.tcp_keepalive_probes
    # or
    #     cat /proc/sys/net/ipv4/tcp_keepalive_probes
    # You can change the value to N.
    #      sudo sysctl -w net.ipv4.tcp_keepalive_probes=<N>
    # or make the change permanently in "/etc/sysctl.conf".
    keep_alive_probes = 9

    # limit the number of outstanding connections in the socket's listen
    # queue. The value must be less than
    #     cat /proc/sys/net/core/somaxconn
    # or
    #     sysctl net.core.somaxconn
    # You can change the value to N.
    #      sudo sysctl -w net.core.somaxconn=<N>
    # or make the change permanently in "/etc/sysctl.conf".
    # The default value of 'somaxconn' is 128.
    _request_queue_size = 5

    def __init__(self, address, request_handler=TCPRequestHandler, timeout=None, ipv4only=True):
        '''Create an instance of TCP server.

        @param address server address, 2-tuple (host, port). An host of '' or port
                       0 tells the OS to use the default.
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
        if self.enable_keep_alive:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, self.keep_alive_time)
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.keep_alive_intvl)
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.keep_alive_probes)
        if __debug__:
            # Re-use binding address for debugging purpose
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(address)
        self.server_address = self._sock.getsockname()
        self._sock.listen(self._request_queue_size)

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
                    events = self.sel.select(timeout)
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


class UDPRequest(object):
    '''A UDP request over IPv4/IPv6.
    '''

    def __init__(self, ipv4only=True):
        '''Create a UDP request over IPv4/IPv6.

        @param ipv4only True for IPv4 only, False for both IPv6/IPv4.
        @exception ValueError parameter error
        @exception OSError <code>socket</code> error

        @see getsockname()
        @see getpeername()
        @see recv_into()
        '''
        self._sock = None

        if ipv4only:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:  # both IPv6 and IPv4, prefer to IPv6
            host, port = addr
            err = None
            for res in socket.getaddrinfo(host, port, 0, socket.SOCK_DGRAM):
                family, socktype, proto, canonname, sockaddr = res
                self._sock = None
                try:
                    self._sock = socket(family, socktype, proto)
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

    def send(self, data, addr):
        '''Send data to server.

        @param addr server address, 2-tuple of (host, port).
        @exception OSError <code>socket</code> error
        '''
        self._sock.sendto(data, addr)

    def recv(self, nbytes):
        '''Receive data from server.

        @param nbytes up to <code>nbytes</code> bytes to received
        @param addr server address, 2-tuple of (host, port).
        @return a bytes object representing the data received
        @exception OSError <code>socket</code> error

        For best match with hardware and network realities, the value of
        <code>nbytes</code> should be a relatively small power of 2, for
        example, <value>4096</value>.
        '''
        data, addr = self._sock.recvfrom(nbytes)
        return data


class UDPRequestHandler(BaseRequestHandler):
    '''UDP request handler.
    '''
    pass


class UDPServer(object):
    '''UDP Server (Only supported for IPv4).
    '''

    address_family = socket.AF_INET
    socket_type = socket.SOCK_DGRAM

    def __init__(self, address, request_handler, ipv4only=True):
        '''Create an instance of TCP server.

        @param address server address, 2-tuple (host, port). An host of '' or port
                       0 tells the OS to use the default.
        @param request_handler request handler class
        @param ipv4only True for IPv4 only, False for both IPv6/IPv4
        @exception OSError <code>socket</code> error
        '''

        self._RequestHandler = request_handler

        # Setup
        self._sock = socket.socket(self.address_family, self.socket_type)
        if __debug__:
            # Re-use binding address for debugging purpose
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(address)
        self.server_address = self._sock.getsockname()

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

                self._handle_one_request()

                if __debug__:
                    print('\n', file=sys.stderr)
        finally:
            self.close()

    def _handle_one_request(self):
        '''Handle single one request.

        @exception OSError <code>socket</code> error
        '''
        self._RequestHandler(self._sock, self)

    def close(self):
        '''Close the server.
        '''
        self._sock.close()


class HTTPServer(TCPServer):
    '''HTTP/1.1 server (Only supported for IPv4).
    '''

    def __init__(self, address, request_handler=TCPRequestHandler, timeout=None, ipv4only=True):
        '''Create an instance of TCP server.

    @param address server address, 2-tuple (host, port). An host of '' or port
                   0 tells the OS to use the default.
    @param request_handler request handler class
    @param timeout timeout of socket object. None for blocking, 0.0 for
                   non-blocking, others for timeout in seconds (float)
    @param ipv4only True for IPv4 only, False for both IPv6/IPv4.
    @exception OSError <code>socket</code> error
    '''
        super(HTTPServer, self).__init__(address, request_handler, timeout, ipv4only)
        self.fqdn = self._sock.getfqdn(self.server_address[0])


class HTTPRequestHandler(TCPRequestHandler):
    '''HTTP request handler.
    '''
    
    http_version = 'HTTP/1.1'

    # 服务器可处理的最大实体数据大小
    max_body_len = 65537

    # 服务器可处理的URL最长长度
    max_url_len = 10240

    # Table mapping response codes to messages; entries have the
    # form {code: (shortmessage, longmessage)}.
    # See RFC 2616 and 6585.
    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
              'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),
        428: ('Precondition Required',
              'The origin server requires the request to be conditional.'),
        429: ('Too Many Requests', 'The user has sent too many requests '
              'in a given amount of time ("rate limiting").'),
        431: ('Request Header Fields Too Large', 'The server is unwilling to '
              'process the request because its header fields are too large.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
        511: ('Network Authentication Required',
              'The client needs to authenticate to gain network access.'),
        }

    def handle(self):
        client_address = self.request.getsockname()
        try:
            data = self.request.recv(max_body_len)
            if len(data) > max_body_len - 1:
                self.request_line = ''
                self.command = ''
                self._send_error(413)
                pass # 413
            if __debug__:
                print('HTTP data from {0}: {1}'.format(client_address, data), file=sys.stderr)

            data = b'response'
            self.request.sendall(data)
            print('Data to {0}: {1}'.format(client_address, data))
        except OSError as err:
            print('Data R/W error {}:'.format(err), file=sys.stderr)
            raise

    def _send_error(code):
        if __debug__:
            print('code={}, message="{}"'.format(code, responses[code][1]))
