#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest,sys
from base.run import Run
from base.utils import log,Conf


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

    self_args = sys.argv[1:]
    #获取命令行参数中的用例执行作用域

    pytest.main(run.get_run_args() + self_args)
    #对pytest的运行传入参数

    run.generate_report()


