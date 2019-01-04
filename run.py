#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest,sys
from multiprocessing import Pool
from base.run import Run
from base.utils import log,Conf
from base.shell import Shell


"""
run all case:
    python3 run.py

run one module case:
    python3 run.py test/test_demo.py

run case with key word:
    python3 run.py -k <keyword>
run class case:
    python3 run.py  test/test_demo.py::Test_demo
run class::method case:
    python3 run.py  test/test_demo.py::Test_demo::test_home
"""

if __name__ == '__main__':


    platform=Conf().androidname  #android  or  ios

    run=Run(platform)


    #获取命令行参数中的用例执行作用域
    run.exec(sys.argv[1:])


    run.generate_report()


