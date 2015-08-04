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

'''Test TCP server over IPv4 in non-blocking mode with <code>select()</code>
I/O multiplex.

'''

import sys
from contextlib import closing

import net


class MyTCPRequestHandler(net.TCPRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(1024)
            print('Data from {0}: {1}'.format(self.client_address, data))

            data = b'response'
            self.request.sendall(data)
            print('Data to {0}: {1}'.format(self.client_address, data))
        except OSError as err:
            print('Data R/W error {}:'.format(err), file=sys.stderr)
            raise


if __name__ == '__main__':
    try:
        with closing(net.TCPServer(('', 8888), \
                request_handler=MyTCPRequestHandler, timeout=0.0)) as srv:
            srv.run()
    except OSError as err:
        print('TCP server failed: {}'.format(err), file=sys.stderr)
