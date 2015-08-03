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

'''Test TCP request over IPv4.

'''

import sys
from contextlib import closing

import net


# Server address
server_addr = ('localhost', 8888)

# Request parameters for testing cases
# Format: (timeout, reconn, wait_time, increase_time)
req_params = (
    # blocking, re-connect disabled (Default)
    (None, 0, 0.0, 0.0),

    # blocking, re-connect enabled
    (None, 3, 0.0, 0.0),
    (None, 3, 2.5, 0.0),
    (None, 3, 2.5, 1.5),

    # timeout, re-connect disabled
    (1.0, 0, 0.0, 0.0),

    # timeout, re-connect enabled
    (1.0, 3, 0.0, 0.0),
    (1.0, 3, 2.5, 0.0),

    # non-blocking, re-connect disabled
    (0.0, 0, 0.0, 0.0),  # ValueError
)


if __name__ == '__main__':
    for param in req_params:
        try:
            with closing(net.TCPRequest(server_addr, *param)) as req:
                print(req)
                data = b'AAA'
                req.send(data)
                print('Send data: {}'.format(data))
                data = req.recv(1024)
                print('Receive data: {}'.format(data))
        except ValueError as err:
            print('Parameter error: {}'.format(err), file=sys.stderr)
        except OSError as err:
            print('Error: {}'.format(err), file=sys.stderr)
