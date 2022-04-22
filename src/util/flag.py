#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: flag.py
@Desc: None
"""
import argparse
import sys


class Flag(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="海关数据爬虫", usage="python main.py hs_code")
        self.args = None

    def register(self):
        self.parser.add_argument("hs", type=str, help="customs HS code")
        self.parser.add_argument("-c", "--criteria", type=str, help="进/出口, value: exports|imports, default exports",
                                 default="exports")
        self.args = self.parser.parse_args()

        return self

    def validate(self):
        if self.args.criteria != "exports" and self.args.criteria != "imports":
            print("error: The criteria flag must be exports or imports.")
            sys.exit(0)
