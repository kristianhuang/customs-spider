#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: flag.py
@Desc: None
"""
import argparse


def register():
    parser = argparse.ArgumentParser(description="海关数据爬虫", usage="python main.py hs_code")
    parser.add_argument("hs", type=str, help="customs HS code")

    return parser.parse_args()
