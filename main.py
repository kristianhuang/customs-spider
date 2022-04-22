#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: main.py
@Desc: None
"""

from src.util import excel, flag
from src.webdriver import WebDriver

if __name__ == '__main__':
    f = flag.Flag()
    f.register().validate()

    wd = WebDriver()
    datas = wd.fetchCustoms(f.args.hs, f.args.criteria)
    excel.save(f"hs-{f.args.hs}-type-{f.args.criteria}", datas)
