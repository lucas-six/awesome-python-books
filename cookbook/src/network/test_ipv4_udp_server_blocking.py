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

'''Test UDP server over IPv4 in blocking mode.

'''

import sys
from contextlib import closing

import net


class MyUDPRequestHandler(net.UDPRequestHandler):
    def handle(self):
        try:
            data, addr = self.request.recvfrom(1024)
            print('Data from {0}: {1}'.format(addr, data))

            data = b'response'
            self.request.sendto(data, addr)
            print('Data to {0}: {1}'.format(addr, data))
        except OSError as err:
            print('Data R/W error {}:'.format(err), file=sys.stderr)
            raise


if __name__ == '__main__':
    try:
        with closing(net.UDPServer(('', 8888), request_handler=MyUDPRequestHandler)) as srv:
            srv.run()
    except OSError as err:
        print('UDP server failed: {}'.format(err), file=sys.stderr)
