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

'''Queue - 线程中队列的使用样例
'''

import threading
import queue
from collections import deque


q = queue.Queue(maxsize=10)


def producer(name, data, times):
    print('Run thread "Producer" {}'.format(name))
    while times > 0:
        times -= 1
        q.put(data)
        print('Thread {0} put()'.format(name))


def cusumer(name, times):
    print('Run thread "Cusumer" {}'.format(name))
    while times > 0:
        times -= 1
        data = q.get()
        q.task_done()
        print('Thread {0} get() {1}'.format(name, data))


class MyQueue(object):
    '''My own multi-producer, multi-cusumer queues.

    @see queue
    '''

    def __init__(self, maxsize=0):
        self._maxsize = maxsize
        self._init_queue(maxsize)
        self._lock = threading.Lock()

        # Notify `_cond_not_empty` whenever an item is added to the queue; a
        # thread waiting to get is notified then.
        self._cond_not_empty = threading.Condition(self._lock)

        # Notify `_cond_not_full` whenever an item is removed from the queue;
        # a thread waiting to put is notified then.
        self._cond_not_full = threading.Condition(self._lock)

        # Notify `_cond_all_tasks_done` whenever the number of unfinished
        # tasks drops to zero; thread waiting to `join()` is notified to
        # resume.
        self._cond_all_tasks_done = threading.Condition(self._lock)
        self._unfinished_tasks = 0

    def qsize(self):
        '''Return the queue actual size. (NOT reliable)'''
        with self._lock:
            return self._queue_size()

    def empty(self):
        '''Check if the queue is empty. (NOT reliable)'''
        with self._lock:
            return self._queue_size() == 0

    def full(self):
        '''Check if the queue is full. (NOT reliable)'''
        with self._lock:
            return 0 < self._queue_size() == self._maxsize

    def task_done(self):
        '''Indicate that a formerly enqueued task is finished.

        Used by Queue cusumer threads,. For each `get()` used to fetch a task,
        a subsequent call to `task_done()` tells that the processing on the
        task is finished.

        If a `join()` is currently blocking, it will resume when all items
        have been processed.
        '''
        with self._cond_all_tasks_done:
            unfinished = self._unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self._cond_all_tasks_done.notify_all()
            self._unfinished_tasks = unfinished

    def join(self):
        '''Block until all items in the queue have been processed.'''
        with self._cond_all_tasks_done:
            while self._unfinished_tasks != 0:
                self._cond_all_tasks_done.wait()

    def get(self):
        '''Get an item from the queue.'''
        with self._cond_not_empty:
            while self._queue_size() == 0:
                self._cond_not_empty.wait()
            item = self._get()
            self._cond_not_full.notify()
            return item

    def put(self, item):
        '''Put an item into the queue.'''
        with self._cond_not_full:
            if self._maxsize > 0:
                while self._queue_size() == self._maxsize:
                    self._cond_not_full.wait()

            self._put(item)
            self._unfinished_tasks += 1
            self._cond_not_empty.notify()

    def _init_queue(self, maxsize):
        '''Initialize the queue representation.'''
        if maxsize == 0:
            self._queue = deque()
        else:
            self._queue = deque(maxlen=maxsize)

    def _queue_size(self):
        return len(self._queue)

    def _put(self, item):
        '''Put an item in the queue.'''
        self._queue.append(item)

    def _get(self):
        '''Get an item from a queue.'''
        return self._queue.popleft()


def test_myqueue():

    q = MyQueue(maxsize=10)

    def producer_test(name, times, data):
        while times > 0:
            times -= 1
            q.put(data)
            print('MyQueue: Thread {0} put'.format(name))

    def cusumer_test(name, times):
        while times > 0:
            times -= 1
            print('MyQueue: Thread {0} get {1}'.format(name, q.get()))
            q.task_done()

    p = threading.Thread(target=producer_test, args=('a', 10, 'data'))
    c = threading.Thread(target=cusumer_test, args=('b', 10))
    p.start()
    c.start()
    p.join()
    c.join()
    q.join()


if __name__ == '__main__':
    threads = []
    t = threading.Thread(target=producer, args=('a','data', 5))
    threads.append(t)
    t = threading.Thread(target=cusumer, args=('b', 5))
    threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    test_myqueue()
