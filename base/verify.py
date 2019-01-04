# -*- coding: utf-8 -*-
import re
from base.utils import log

class NotFoundElementError(Exception):
    pass


class NotFoundTextError(Exception):
    pass


class NumError(Exception):
    pass






class Assert():

    def _raise_exception(self, msg):

        raise AssertionError(msg)


    def assert_true(self, condition, msg=None,logmsg=''):
        if not condition:
            self._raise_exception(msg)
        else:
            log.info("断言成功: {}".format(logmsg))

    def assert_false(self, false_condition, msg=None,logmsg=''):
        if false_condition:
            self._raise_exception(msg)
        else:
            log.info("断言成功: {}".format(logmsg))

    def assert_equals(self, expected, actual, msg=None,logmsg=''):
        self.assert_true(expected == actual, msg,logmsg)

    assert_eq = assert_equals

    def assert_not_equals(self, expected, actual, msg=None,logmsg=''):
        self.assert_true(expected != actual, msg,logmsg)

    assert_ne = assert_not_equals


    def assert_in(self, member, container, msg=None,logmsg=''):
        self.assert_true(member in container, msg,logmsg)

    def assert_not_in(self, member, container, msg=None,logmsg=''):
        self.assert_true(member not in container, msg,logmsg)

    def assert_greater_than(self, greater, less, msg=None,logmsg=''):
        self.assert_true(greater > less, msg,logmsg)

    assert_gt = assert_greater_than

    def assert_greater_than_equals(self, expected, actual, msg=None,logmsg=''):
        self.assert_true(actual >= expected, msg,logmsg)

    assert_gte = assert_greater_than_equals

    def assert_less_than_equals(self, expected, actual, msg=None,logmsg=''):
        self.assert_true(actual <= expected, msg,logmsg)

    assert_lte = assert_less_than_equals


    def assert_match(self, pattern, s, flags=0, msg=None,logmsg=''):
        """使用 re.match 进行匹配断言测试，注意与 assert_search 的区别
        """
        self.assert_true(re.match(pattern, s, flags) is not None, msg,logmsg)

    def assert_full_match(self, pattern, s, flags=0, msg=None,logmsg=''):
        """使用 re.fullmatch 进行匹配断言测试"""
        self.assert_true(re.fullmatch(pattern, s, flags) is not None, msg,logmsg)

    def assert_search(self, pattern, s, flags=0, msg=None,logmsg=''):
        """使用 re.search 进行搜索断言测试"""
        self.assert_true(re.search(pattern, s, flags), msg,logmsg)


Validator=Assert()