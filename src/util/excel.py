#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File: excel.py
@Desc: None
"""
import os

import pandas as pd


def save(name: str, data):
    """
    create excel

    :param name: file name
    :param data: datas
    :return:
    """
    df = pd.DataFrame(data)
    df.to_excel(f"{os.path.dirname(__file__)}/../../data/{name}.xlsx", sheet_name='Sheet1', engine='xlsxwriter')
