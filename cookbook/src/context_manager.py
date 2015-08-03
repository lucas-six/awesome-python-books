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

'''Context Manager - 上下文管理器

此菜谱包含：

- 自定义上下文管理器
- 上下文管理器注解示例
- 自定义上下文管理器注解

<code>with</code>语句支持运行时上下文。

@see http://www.python.org/dev/peps/pep-0343/

'''


class MyContextManager(object):
    '''自定义上下文管理器
    '''

    def __init__(self):
        '''初始化上下文管理器

        可抛出异常
        '''
        pass

    def __enter__(self):
        return self

    def __exit__(self, etype, evalue, traceback):
        if etype is not None:
            print(etype, evalue, traceback)
        self.close()

    def close(self):
        '''清理上下文管理器
        '''
        pass

    def do(self):
        '''上下文处理函数
        
        可抛出异常
        '''
        pass


# 上下文管理器注解示例
from contextlib import contextmanager

@contextmanager
def closing(thing):
    '''contextlib.closing()的参考实现

    @see contextlib#closing()
    '''
    try:
        yield thing
    finally:
        thing.close()


# 自定义上下文管理器注解
#
# @see contextlib.ContextDecorator
# @since Python 3.2
from contextlib import ContextDecorator

stack = []
class mycontext(ContextDecorator):
    '''自定义上下文管理器注解
    '''

    def __enter__(self):
        stack.append('Enter')
        return self

    def __exit__(self, *exc): # etype, evalue, traceback
        stack.append('Exit')
        return False

@mycontext()
def mycontextfunc():
    stack.append('Do')

mycontextfunc()
assert stack == ['Enter', 'Do', 'Exit']
