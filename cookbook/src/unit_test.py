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

'''Unit Testing - 单元测试

此菜谱包含：

- 单元测试unittest使用样例
- PEP 8测试
- 自定义的PyUnit

'''

import unittest

import pep8


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


class CodeStyleTestCase(unittest.TestCase):

    def test_pep8_conformance(self):
        pep8_style = pep8.StyleGuide(quiet=False)
        result = pep8_style.check_files([__file__])
        self.assertEqual(result.total_errors, 0,
                         'Found {0} code style errors (and warnings)'
                         .format(result.total_errors))


class MyPyUnit(object):
    '''My own unit testing framework, based on Erich Gamma's JUnit and Kent
    Beck's Smalltalk testing framework.

    Acknowledge to the book "Test-Driven Development: By Examples".

    Further information is available in the bundled documentation, and from

        http://docs.python.org/3/library/unittest.html

    '''

    _test_suite = []

    class TestCase(object):
        '''A class whose instances are single test cases.

        If the fixture may be used for many test cases, create as
        many test methods as are needed. When instantiating such a TestCase
        subclass, specify in the constructor arguments the name of the test
        method that the instance is to execute.

        Test authors should subclass TestCase for their own tests. Construction
        and clean up of the test's environment ('fixture') can be implemented
        by overriding the `setUp` and `tearDown` methods respectively.

        If it is necessary to override the `__init__` method, the base class
        `__init__` method must always be called. It is important that
        subclasses should not change the signature of their `__init__` method,
        since instances of the classes are instantiated automatically by parts
        of the framework in order to be run.
        '''

        def __init__(self):
            self.tests = 0  # number of test cases
            self.errors = 0  # number of errors
            self.verbosity = 1

        def setUp(self):
            '''Hook method for setting up the test fixture before exercising
            it.

            Test authors should override this method in the subclass of
            TestCase to construct the test's environment ('fixture')
            respectively.
            '''
            pass

        def tearDown(self):
            '''Hook method for cleaning up the test fixture after testing it.

            Test authors should override this method in the subclass of
            TestCase to clean up the test's environment ('fixture')
            respectively.
            '''
            pass

        def run(self):
            for test_method_name in dir(self):
                if test_method_name.startswith('test_'):
                    test_method = getattr(self, test_method_name)
                    self.tests += 1
                    self.setUp()
                    if self.verbosity == 2:
                        print('{0} ...'.format(test_method_name))
                    try:
                        test_method()
                    finally:
                        self.tearDown()

        def summary(self):
            '''Returns a summary of the testing report, that includes
            information of the number of test cases being run and how many
            failed cases occur.

            @return String of testing report summary.
            '''
            return '\nTest Summary: {0} run, {1} failed'.format(self.tests,
                                                                self.errors)

        def assertTrue(self, exp):
            '''Check that the expression is true.

            @param exp Expression to be checked.
            '''
            if not exp:
                self.errors += 1

        def assertEqual(self, obj1, obj2):
            '''Check that the two given objects are equal.

            @param obj1 The first checked object.
            @param obj2 The second checked object.
            '''
            self.assertTrue(obj1 == obj2)

        def assertGreater(self, obj1, obj2):
            '''Check that the first given object is greater than the second one.

            @param obj1 The first checked object.
            @param obj2 The second checked object.
            '''
            self.assertTrue(obj1 > obj2)

        def assertLess(self, obj1, obj2):
            '''Check that the first given object is less than the second one.

            @param obj1 The first checked object.
            @param obj2 The second checked object.
            '''
            self.assertTrue(obj1 < obj2)

        def assertGreaterEqual(self, obj1, obj2):
            '''Check that the first given object is greater than or equals to
            the second one.

            @param obj1 The first checked object.
            @param obj2 The second checked object.
            '''
            self.assertTrue(obj1 >= obj2)

        def assertLessEqual(self, obj1, obj2):
            '''Check that the first given object is less than or equals to the
            second one.

            @param obj1 The first checked object.
            @param obj2 The second checked object.
            '''
            self.assertTrue(obj1 <= obj2)

    class TestSuite(object):
        '''A test suite is a composite test consisting of a number of
        TestCases.

        For use, create an instance of TestSuite, then add test case instances.
        When all tests have been added, the suite can be passed to a test
        runner, such as run(). It will run the individual test cases
        in the order in which they were added, aggregating the results. When
        subclassing, do not forget to call the base class constructor.
        '''
        def __init__(self):
            self.suite = []

        def addTestCase(self, test_case):
            '''Add test case instance.

            If the given object is not the instance of TestCase, nothing to be
            done.

            @param test_case test case instance that is added.
            '''
            if isinstance(test_case, MyPyUnit.TestCase):
                self.suite.append(test_case)

        def addTestCaseFromClass(self, test_case):
            '''Add test case.

            If the given class is not the subclass of the TestCase, nothing to
            be done.

            @param test_case class of test case that is added.
            '''
            if issubclass(test_case, MyPyUnit.TestCase):
                self.suite.append(test_case())

        def run(self):
            '''Run all the test cases in this test suite, and print a testing
            report summary for each test case.'''
            for test_case in self.suite:
                test_case.run()
                print(test_case.summary())


class MyPyUnitTestCase(MyPyUnit.TestCase):

    def setUp(self):
        self.verbosity = 2

    def test_a(self):
        pass

    def test_b(self):
        self.assertTrue(1 == 1)

    # @unittest.expectedFailure
    def test_c(self):
        self.assertTrue(1 == 2)

    def test_d(self):
        self.assertEqual(1, 1)

    # @unittest.expectedFailure
    def test_e(self):
        self.assertEqual(1, 2)

    # @unittest.expectedFailure
    def test_f(self):
        self.assertGreater(1, 1)

    # @unittest.expectedFailure
    def test_g(self):
        self.assertGreater(1, 2)

    def test_h(self):
        self.assertGreater(2, 1)

    # @unittest.expectedFailure
    def test_i(self):
        self.assertLess(1, 1)

    def test_j(self):
        self.assertLess(1, 2)

    # @unittest.expectedFailure
    def test_k(self):
        self.assertLess(2, 1)

    def test_l(self):
        self.assertGreaterEqual(1, 1)

    # @unittest.expectedFailure
    def test_m(self):
        self.assertGreaterEqual(1, 2)

    def test_n(self):
        self.assertGreaterEqual(2, 1)

    def test_o(self):
        self.assertLessEqual(1, 1)

    def test_p(self):
        self.assertLessEqual(1, 2)

    # @unittest.expectedFailure
    def test_q(self):
        self.assertLessEqual(2, 1)


if __name__ == '__main__':
    suite = MyPyUnit.TestSuite()
    suite.addTestCase(MyPyUnitTestCase())
    suite.addTestCaseFromClass(MyPyUnitTestCase)
    suite.run()  # 8 failed

    unittest.main(verbosity=2, catchbreak=True)
