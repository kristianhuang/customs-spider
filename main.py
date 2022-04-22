#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: main.py
@Desc: None
"""

from src.util import excel, flag
from src.webdriver import WebDriver

if __name__ == '__main__':
    args = flag.register()
    wd = WebDriver()
    datas = wd.fetchCustoms(args.hs)
    excel.save(datas)
