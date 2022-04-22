#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: main.py
@Desc: None
"""

from src.util import excel
from src.webdriver import WebDriver

if __name__ == '__main__':
    wd = WebDriver()
    datas = wd.fetchCustoms("460212")
    excel.save(datas)
