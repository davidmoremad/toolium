# -*- coding: utf-8 -*-
u"""
Copyright 2015 Telefónica Investigación y Desarrollo, S.A.U.
This file is part of Toolium.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import unittest

import mock
from nose.tools import assert_true, assert_false

from toolium.test_cases import BasicTestCase


class MockTestClass(BasicTestCase):
    def setUp(self):
        root_path = os.path.dirname(os.path.realpath(__file__))
        self.config_files.set_config_directory(os.path.join(root_path, 'conf'))
        super(MockTestClass, self).setUp()

    def mock_pass(self):
        pass

    def mock_fail(self):
        raise AssertionError('test error')


def run_mock(test_name):
    """Run a unit test from mock class

    :param test_name: test name that must be executed
    :returns: test instance
    """
    suite = unittest.TestSuite()
    test = MockTestClass(test_name)
    suite.addTest(test)
    unittest.TextTestRunner().run(suite)
    return test


class BasicTestCaseTests(unittest.TestCase):
    def setUp(self):
        # Configure logger mock
        self.logger = mock.MagicMock()
        self.logger_patch = mock.patch('logging.getLogger', mock.MagicMock(return_value=self.logger))
        self.logger_patch.start()

    def tearDown(self):
        self.logger_patch.stop()

    def test_tear_down_pass(self):
        test = run_mock('mock_pass')
        assert_true(test._test_passed)

        # Check logging messages
        init_message = 'Running new test: MockTestClass.mock_pass'
        expected_response = "The test 'MockTestClass.mock_pass' has passed"
        self.logger.info.assert_has_calls([mock.call(init_message), mock.call(expected_response)])

    def test_tear_down_fail(self):
        test = run_mock('mock_fail')
        assert_false(test._test_passed)

        # Check logging error messages
        init_message = 'Running new test: MockTestClass.mock_fail'
        expected_response = "The test 'MockTestClass.mock_fail' has failed: test error"
        self.logger.info.assert_called_once_with(init_message)
        self.logger.error.assert_called_once_with(expected_response)
