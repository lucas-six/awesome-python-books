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

'''Iterator - 迭代器

此菜谱包含：

- 自定义迭代器及使用样例
- 用迭代器简化代码
- 自定义生成器
- 自定义生成器类型判断
- 自定义生成器使用样例

'''


class MyIterator(object):
    '''自定义迭代器
    '''

    def __init__(self, seq):
        self._container = seq
        self._index = -1

    def __iter__(self):
        return iter(self._container)

    def __next__(self):
        if self._index == len(self._container) - 1:
            raise StopIteration
        self._index += 1
        return self._container[self._index]

    def __reversed__(self):
        pass


# 自定义迭代器使用样例
mylist = [1, 2, 3]
for item in MyIterator(mylist):
    assert item in mylist


# 用迭代器简化代码
def get_sth():
    return 'b'

def do_sth(a):
    pass

# 可简化代码：
#
# while True:
#    a = get_sth()
#    if a == 'b':
#        break
#    do_sth(a)
for a in iter(get_sth, 'b'):
    do_sth(a)


def my_generator(n):
    '''自定义生成器

    Python的生成器提供了一种简洁的实现迭代器的方式 (yield语句)

    '''
    while True:
        yield n
        n += 1

# 自定义生成器类型判断
assert type(my_generator).__name__ == 'function'
assert type(my_generator(10)).__name__ == 'generator'
import types
assert isinstance(my_generator, types.FunctionType)
assert isinstance(my_generator(10), types.GeneratorType)


# 自定义生成器使用样例
container = []
for i in my_generator(0):
    if len(container) == 3:
        break
    container.append(i)
assert container == [0, 1, 2]
