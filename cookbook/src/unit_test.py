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

'''Unit Testing - 单元测试

此菜谱包含：

- int类型格式化字符串
- float类型格式化字符串

'''

import unittest


class StringTestCase(unittest.TestCase):

    def test_capitalize(self):
        self.assertEqual(' hello '.capitalize(), ' hello ')
        self.assertEqual('Hello '.capitalize(), 'Hello ')
        self.assertEqual('hello '.capitalize(), 'Hello ')
        self.assertEqual('HeLLo '.capitalize(), 'Hello ')
        with self.assertRaises(TypeError):
            'hello'.capitalize(0)

    def test_lower(self):
        self.assertEqual('HeLLo'.lower(), 'hello')
        self.assertEqual('hello'.lower(), 'hello')
        with self.assertRaises(TypeError):
            'hello'.lower(0)

    def test_upper(self):
        self.assertEqual('HeLLo'.upper(), 'HELLO')
        self.assertEqual('HELLO'.upper(), 'HELLO')
        with self.assertRaises(TypeError):
            'hello'.upper(0)
