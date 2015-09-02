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

'''Semaphore - 线程信号量样例
'''

import threading


share = []
semaphore = threading.BoundedSemaphore(5)


def producer(name, data):
    print('Run thread "Producer" {}'.format(name))

    # Same with:
    #
    #     semaphore.acquire()
    #     share.append(data)
    #     print(share)
    #     semaphore.release()
    #
    with semaphore:
        # Python 2: semaphore._Semaphore__value
        print('Thread {0}: Semaphore value is {1}'.format(name, semaphore._value))
        share.append(data)
        print(share)


def cusumer(name, data):
    print('Run thread "Cusumer" {}'.format(name))
    with semaphore:
        # Python 2: semaphore._Semaphore__value
        print('Thread {0}: Semaphore value is {1}'.format(name, semaphore._value))
        if len(share) > 0:
            share.pop()
        print(share)


if __name__ == '__main__':
    threads = []
    t = threading.Thread(target=producer, args=('a',1))
    threads.append(t)
    t = threading.Thread(target=cusumer, args=('b',2))
    threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
