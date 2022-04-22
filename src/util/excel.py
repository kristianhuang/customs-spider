#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: excel.py
@Desc: None
"""
import os

import pandas as pd


def save(data):
    df = pd.DataFrame(data)
    df.to_excel(f"{os.path.dirname(__file__)}/../../data/demo.xlsx", sheet_name='Sheet1', engine='xlsxwriter')
